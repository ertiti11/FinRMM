/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("agent_updates_collection")

  // remove field
  collection.fields.removeById("url3677735735")

  // add field
  collection.fields.addAt(9, new Field({
    "hidden": false,
    "id": "file3677735735",
    "maxSelect": 1,
    "maxSize": 0,
    "mimeTypes": [],
    "name": "file_url",
    "presentable": false,
    "protected": false,
    "required": true,
    "system": false,
    "thumbs": [],
    "type": "file"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("agent_updates_collection")

  // add field
  collection.fields.addAt(2, new Field({
    "exceptDomains": [],
    "hidden": false,
    "id": "url3677735735",
    "name": "file_url",
    "onlyDomains": [],
    "presentable": false,
    "required": true,
    "system": false,
    "type": "url"
  }))

  // remove field
  collection.fields.removeById("file3677735735")

  return app.save(collection)
})
