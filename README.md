# tastingswithtay-iac
Resources supporting the management and creation of the infrasture for `tastingswithtay`.


## Tree
```
 % tree
.
├── README.md
├── buildspec.yml
├── foundation.yaml
├── images
│   └── temp.jpeg
├── lambda
│   ├── auth
│   │   └── auth.py
│   └── content
│       ├── content.py
│       └── dynamodb_wrapper.py
└── stacks
    ├── api.yaml
    ├── compute.yaml
    ├── networking.yaml
    ├── pipeline.yaml
    └── storage.yaml
```