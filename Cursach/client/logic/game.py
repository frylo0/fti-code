import storage
import requests
import json
from flask import request
import threading


def handle():
   storage.add_response_handler('connect', on_game_connect)
   
   storage.add_response_handler('figure-select', on_figure_select)
   storage.add_response_handler('figure-unselect', on_figure_unselect)
   
   storage.add_response_handler('connection-count-update', on_connection_count_update)
   storage.add_response_handler('ready-count-update', on_ready_count_update)


def on_game_connect(req):
   print('On connect: thread is', threading.get_ident())
   
   print('On connect: Post')
   connection_count = req['connection_count']
   storage.connetion_count = connection_count
   
   storage.add_task('setConnectionCount', connection_count)

   return '{"status": "OK"}'



def on_figure_select(req):
   if int(req['sender_id']) != storage.id:
      storage.add_task('otherFigureSelect', req['figure'])
   return '{"status": "OK"}'
   
def on_figure_unselect(req):
   if int(req['sender_id']) != storage.id:
      storage.add_task('otherFigureUnselect', req['figure'])
   return '{"status": "OK"}'

def on_ready_count_update(req):
   storage.add_task('setReadyCount', req['count'])
   return '{"status": "OK"}'
def on_connection_count_update(req):
   storage.connection_count = int(req['count'])
   storage.add_task('setConnectionCount', req['count'])
   return '{"status": "OK"}'

   
def get_game_sid(callback):
   callback.Call(storage.sid)
   
def get_connection_count(callback):
   callback.Call(storage.connection_count)
def get_skin(callback):
   res = storage.gameload('get-skin', {})
   callback.Call(res['skin'])
def get_connections_state(callback):
   res = storage.gameload('get-connections-state', {})
   callback.Call(res)


def send_figure_select(figure_type):
   storage.gameload('figure-select', {
      'figure': figure_type,
   })
def send_figure_unselect(figure_type):
   storage.gameload('figure-unselect', {
      'figure': figure_type,
   })
def send_figure_change(old_figure_type, new_figure_type):
   storage.gameload('figure-unselect', {
      'figure': old_figure_type,
   })
   storage.gameload('figure-select', {
      'figure': new_figure_type,
   })

def send_ready():
   storage.gameload('ready', {})
def send_unready():
   storage.gameload('unready', {})
   
def send_disconnect():
   storage.gameload('disconnect', {})
   storage.connection_process.terminate()
   

get_task_counter = 0
def get_tasks(callback):
   global get_task_counter
   get_task_counter += 1
   if not storage.tasks.empty():
      #print('getTasks: storage.tasks is', storage.tasks)
      tasks = []
      while not storage.tasks.empty():
         tasks.append(storage.tasks.get())
      print('getTasks: some tasks', '; '.join([f'{t[0]}(' + ', '.join(map(str, t[1])) + ')' for t in tasks]))
      callback.Call(tasks)
   else:
      pass
      #print('getTasks: queue is empty ', get_task_counter)
   

handle()