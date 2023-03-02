from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json

items = []

class TodoItems(RequestHandler):
  def get(self):
    self.write({'items': items})

class TodoItem(RequestHandler):
  def get(self, id):
    global items
    for item in items:
      if item['id'] == int(id):
        self.write({'message': item['name']})

  def post(self, _):
    global items
    new_item = json.loads(self.request.body)
    id_exists = False
    for item in items:
      if item['id'] == int(new_item['id']):
        id_exists = True
    if id_exists:
      self.write({'message': 'item with that id already exists'})
    else:    
      items.append(json.loads(self.request.body))
      self.write({'message': 'new item added'})

  def delete(self, id):
    global items
    item_exists = False
    for item in items:
      if item['id'] == int(id):
        item_exists = True
    if item_exists:   
      new_items = [item for item in items if item['id'] is not int(id)]
      items = new_items
      self.write({'message': 'Item with id %s was deleted' % id})
    else:
      self.write({'message': 'Item with id %s does not exist' % id})

  def put(self, _):
    global items
    edit_item = json.loads(self.request.body)
    item_exists = False
    for item in items:
      if item['id'] == int(edit_item['id']):
        item['name'] = edit_item['name']
        item_exists = True
    if item_exists:
      self.write({'message': 'item edited'})
    else:
      self.write({'message': 'item does not exist'})

def make_app():
  urls = [
    ("/", TodoItems),
    (r"/api/item/([^/]+)?", TodoItem)
    ]
  return Application(urls, debug=True)
  
if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    IOLoop.instance().start()
