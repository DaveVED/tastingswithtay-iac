# tastingswithtay-iac
`CloudFormation` infrastructure as code & `Python3.9` Lambda source code supporting `https://tastingswithtay.com`. Tastingswithtay is a website spun up to support my [wife](https://www.linkedin.com/search/results/all/?fetchDeterministicClustersOnly=true&heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAAA2cmMIBoJJcTrc_KMA9KfnvpC_o09K2LhI&keywords=taylor%20dennis%20cfp%C2%AE&origin=RICH_QUERY_SUGGESTION&position=0&searchId=7814197b-183e-411a-8544-ddf606477752&sid=T%3Bg). Random documentation can be could throughout the code, if you would like to leverage this to mange you 3 tier architecture.

## Architecture

## CI
#### Branching Statergy
#### Pipeline
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