schema = {
  "type": "map",
  "mapping": {
    "vagrant": {
      "type": "map",
      "allowempty": True,
    },
    "runner": {
      "type": "map",
      "mapping": {
        "token": {
          "type": "str",
          "required": True
        },
        "interval": {
          "type": "int",
          "range": {
            "min": 1
          }
        },
        "instances": {
          "type": "int",
          "range": {
            "min": 1
          }
        },
        "endpoint": {
          "type": "str",
          "required": True
        }
      }
    },
    "logging": {
      "type": "map",
      "allowempty": True
    }
  }
}
