/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_3615662572")

  // add field
  collection.fields.addAt(1, new Field({
    "cascadeDelete": false,
    "collectionId": "pbc_2726680096",
    "hidden": false,
    "id": "relation873754891",
    "maxSelect": 1,
    "minSelect": 0,
    "name": "agent_id",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "relation"
  }))

  // add field
  collection.fields.addAt(2, new Field({
    "cascadeDelete": false,
    "collectionId": "pbc_2442875294",
    "hidden": false,
    "id": "relation434858273",
    "maxSelect": 1,
    "minSelect": 0,
    "name": "client_id",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "relation"
  }))

  // add field
  collection.fields.addAt(3, new Field({
    "cascadeDelete": false,
    "collectionId": "pbc_2602490748",
    "hidden": false,
    "id": "relation2377515398",
    "maxSelect": 1,
    "minSelect": 0,
    "name": "task_id",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "relation"
  }))

  // add field
  collection.fields.addAt(4, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text3065852031",
    "max": 0,
    "min": 0,
    "name": "message",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3615662572")

  // remove field
  collection.fields.removeById("relation873754891")

  // remove field
  collection.fields.removeById("relation434858273")

  // remove field
  collection.fields.removeById("relation2377515398")

  // remove field
  collection.fields.removeById("text3065852031")

  return app.save(collection)
})
