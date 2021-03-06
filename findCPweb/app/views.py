# views.py
from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound

from . import models

#import sys, os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from findCPcore import CobraMetabolicModel
from findCPcore import Facade

from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer
import json

from asgiref.sync import async_to_sync


def notify_function(result_ok, error,  model_id, reactions, metabolites, genes, reactions_list, args1=None, args2=None):
	channel_layer = get_channel_layer()
	print("ENVIANDO: ", result_ok)
	if result_ok:
		async_to_sync(channel_layer.send)(args1, {"type":"ws_send", "text":json.dumps({"result":"readComplete", "message":"ok", "model":model_id, "reactions":reactions, "metabolites":metabolites, "genes":genes, "reactions_list":reactions_list}) })
		print("ENVIADO OK")
	else:
		async_to_sync(channel_layer.send)(args1, {"type":"ws_send", "text":json.dumps({"result":"readComplete", "message":error, "model":"null", "reactions":"null", "metabolites":"null", "genes":"null", "reactions_list":"null"}) })


class UploadFile(View):
	def _upload_file(self, request):
		file = request.FILES['fileToUpload']
		arg1 = request.session.__getitem__('channel')
		self.facade = Facade()
		destfile = file.temporary_file_path()
		destfile = destfile[:-12] + '1' + destfile[-12:]
		with open(destfile, 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
		self.facade.read_model(True, destfile, notify_function, args1=arg1)		
		request.session.__setitem__('tid', self.facade.get_tid())
		request.session.__setitem__('file', destfile)
		request.session.set_expiry(900)
		print("tid:", self.facade.get_tid())
		return HttpResponse("success")

	def post(self, request):
		print("POST: Upload file")
		request.upload_handlers.pop(0)
		return self._upload_file(request)


def set_channel(request):
	print(request.POST)
	aux = request.POST['channel'] 
	print("received: " + aux)
	request.session.__setitem__('channel', aux)
	request.session.set_expiry(900)
	print("returning")
	return HttpResponse("success")


def get_cancel(request):
	tid = request.session.__getitem__('tid')
	print("Cancelling:" , tid)
	facade = Facade()
	facade.stop_tid(tid)
	print("Stopped:" , tid)
	return HttpResponse("success")


def get_index(request):
	return render(request, 'index.html', {})


def notify_function_log(text, args1=None, args2=None, ended=False, result=False, error=None):
	channel_layer = get_channel_layer()
	if ended:
		if result:
			async_to_sync(channel_layer.send)(args1, {"type":"ws_send", "text":json.dumps({"result":"workDone", "message":"workDone"}) })
		else:
			if error is None:
				error_msg = ""
			else:
				error_msg = error
			async_to_sync(channel_layer.send)(args1, {"type":"ws_send", "text":json.dumps({"result":"workDone", "message":error_msg}) })
	else:
		async_to_sync(channel_layer.send)(args1,{"type":"ws_send", "text":json.dumps({"result":"log", "message":text}) })


def work(request):
	file_dest = request.session.__getitem__('file')
	args1 = request.session.__getitem__('channel')
	facade = Facade()
	facade.set_model_path(file_dest)	

	task = request.POST['task']
	print("task:", task)
	if task == "SPREAD":
		output =  file_dest[:-4] + ".xls"
		request.session.__setitem__('output', output)
		facade.generate_spreadsheet(True, file_dest,notify_function_log, args1=args1, args2=None, output_path=output)
		request.session.__setitem__('tid', facade.get_tid())
		request.session.set_expiry(900)
	elif task == "DEM":
		output = file_dest[:-4] + ".xml"
		request.session.__setitem__('output', output)
		facade.find_and_remove_dem(True, output, notify_function_log, file_dest, args1=args1, args2=None)
		request.session.__setitem__('tid', facade.get_tid())
		request.session.set_expiry(900)
	elif task == "FVA":
		output = file_dest[:-4] + ".xml"
		request.session.__setitem__('output', output)
		facade.run_fva(True, output, notify_function_log, file_dest, args1=args1, args2=None)
		request.session.__setitem__('tid', facade.get_tid())
		request.session.set_expiry(900)
	elif task == "FVADEM":
		output = file_dest[:-4] + ".xml"
		request.session.__setitem__('output', output)
		facade.run_fva_remove_dem(True, output, notify_function_log, file_dest, args1=args1, args2=None)
		request.session.__setitem__('tid', facade.get_tid())
		request.session.set_expiry(900)

	return HttpResponse("success")

def download_file(request):
	print("hola?")
	try:
		output = request.session.__getitem__('output')
		print("file:", output)
		with open(output, 'rb') as nfile:
			response = HttpResponse(nfile.read())
			if output[-4:] == ".xls":
				response['content_type'] = 'application/vnd.ms-excel'
				response['Content-Disposition'] = 'attachment;filename=result.xls'
			else:
				# xml file
				response['content_type'] = 'application/xml'
				response['Content-Disposition'] = 'attachment;filename=model.xml'
			return response
	except Exception as error:
		raise error
		return HttpResponseNotFound("error with file") 
	
