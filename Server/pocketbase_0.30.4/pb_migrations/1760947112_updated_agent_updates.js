/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("agent_updates_collection")

  // add field
  collection.fields.addAt(1, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text3206337475",
    "max": 0,
    "min": 0,
    "name": "version",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": true,
    "system": false,
    "type": "text"
  }))

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

  // add field
  collection.fields.addAt(3, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text1480854230",
    "max": 0,
    "min": 0,
    "name": "file_hash",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(4, new Field({
    "hidden": false,
    "id": "number3296905238",
    "max": null,
    "min": null,
    "name": "size_mb",
    "onlyInt": false,
    "presentable": false,
    "required": false,
    "system": false,
    "type": "number"
  }))

  // add field
  collection.fields.addAt(5, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text2189808891",
    "max": 0,
    "min": 0,
    "name": "release_notes",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(6, new Field({
    "hidden": false,
    "id": "select2063623452",
    "maxSelect": 1,
    "name": "status",
    "presentable": false,
    "required": true,
    "system": false,
    "type": "select",
    "values": [
      "done",
      "pending",
      "failed"
    ]
  }))

  // add field
  collection.fields.addAt(7, new Field({
    "hidden": false,
    "id": "bool93319235",
    "name": "auto_install",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "bool"
  }))

  // add field
  collection.fields.addAt(8, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text3890410120",
    "max": 0,
    "min": 0,
    "name": "min_version",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(9, new Field({
    "hidden": false,
    "id": "date3882452845",
    "max": "",
    "min": "",
    "name": "release_date",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "date"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("agent_updates_collection")

  // remove field
  collection.fields.removeById("text3206337475")

  // remove field
  collection.fields.removeById("url3677735735")

  // remove field
  collection.fields.removeById("text1480854230")

  // remove field
  collection.fields.removeById("number3296905238")

  // remove field
  collection.fields.removeById("text2189808891")

  // remove field
  collection.fields.removeById("select2063623452")

  // remove field
  collection.fields.removeById("bool93319235")

  // remove field
  collection.fields.removeById("text3890410120")

  // remove field
  collection.fields.removeById("date3882452845")

  return app.save(collection)
})
