# tastingswithtay-iac
Resources supporting the management and creation of the infrasture for `tastingswithtay`, which is a `react` frontend service, with a `serverless` backend spun up to support my [wife](https://www.linkedin.com/search/results/all/?fetchDeterministicClustersOnly=true&heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAAA2cmMIBoJJcTrc_KMA9KfnvpC_o09K2LhI&keywords=taylor%20dennis%20cfp%C2%AE&origin=RICH_QUERY_SUGGESTION&position=0&searchId=7814197b-183e-411a-8544-ddf606477752&sid=T%3Bg). You can view her cooking recipies, stay up to date with our chickens, or see what we're currenlty going in our garden to be used in her recipes. Check it out [here](http://tastingswithtay.com/)!


This `IaC` could also be forked, and used to support any `3 tier` application you wanted to host on `AWS`.

## Bootstraping the Data
When the infastruce is first spun up, you should bootstrap the `dynamdodb` database, and `s3` asset bucket with the intial data needed to support basic functionality. The can be done using the `./lib.scripts/init_dump.py` script. This will.

- [x] Populate the s3 asset bucekt with the images supporting the initial recipes.
- [x] Populate the dynamodb with the intial content (recipes) and the metadata to support those.

Check it out.
```
(.venv) % ./lib/scripts/init_dump.py
2023-04-01 18:08:42,096 - INFO - Loading initial data...
2023-04-01 18:08:42,097 - INFO - Loaded 4 items from JSON file.
2023-04-01 18:08:42,097 - INFO - Loaded 4 items of initial data.
2023-04-01 18:08:42,097 - INFO - Uploading files to S3...
2023-04-01 18:08:45,657 - INFO - Uploaded file dummy/pho.jpg to S3 bucket tastingswithtay-dev-assets
2023-04-01 18:08:47,095 - INFO - Uploaded file dummy/bread.jpg to S3 bucket tastingswithtay-dev-assets
2023-04-01 18:08:48,207 - INFO - Uploaded file dummy/beef.jpg to S3 bucket tastingswithtay-dev-assets
2023-04-01 18:08:49,328 - INFO - Uploaded file dummy/pork.jpg to S3 bucket tastingswithtay-dev-assets
2023-04-01 18:08:49,329 - INFO - Uploaded 4 files to S3.
2023-04-01 18:08:49,330 - INFO - Writing data to DynamoDB...
2023-04-01 18:08:49,552 - INFO - Wrote item with contentId 9f22ea12-c858-4bca-832e-cd477aa61e6e and sortKey beef to DynamoDB table tastingswithtay-dev-content
2023-04-01 18:08:49,607 - INFO - Wrote item with contentId 4a20f690-28e1-4808-84df-a416773f882e and sortKey bread to DynamoDB table tastingswithtay-dev-content
2023-04-01 18:08:49,661 - INFO - Wrote item with contentId 6d5f8b3a-4f08-4ffd-b379-009434409266 and sortKey pho to DynamoDB table tastingswithtay-dev-content
2023-04-01 18:08:49,714 - INFO - Wrote item with contentId 1d6bbc10-bb74-4e47-a459-3ff6b01797b2 and sortKey pork to DynamoDB table tastingswithtay-dev-content
2023-04-01 18:08:49,715 - INFO - Successfully loaded initial data, uploaded files to S3, and wrote data to DynamoDB.
```

## Creating an API Key
The lmabda authoier works with a `Authorization` token passed it it via a header. It will.

- [x] Pull down the `clientId` header.
- [x] Serach `secertsmanager` for that token, if found validate it against the `Authorization` passed in. If the token does not match the clients token or is not passed in, access to API will be denited.

To create a client and a token you can leverage the `./lib/scripts/create_api_keys.py` cli utlity. This will.

- [x] extract the name passed in via cli.
- [x] generate an api key.
- [x] store the mapping between client & api key in secerts manager.

Check it out.
```
(.venv) % ./lib/scripts/create_api_keys.py --name tastingswithtay
2023-04-01 16:01:39,458 - botocore.credentials - INFO - Found credentials in shared credentials file: ~/.aws/credentials
2023-04-01 16:01:39,744 - root - INFO - Created secret tastingswithtay-api-key.
2023-04-01 16:01:39,745 - root - INFO - API key for tastingswithtay stored in Secrets Manager.
```

## Testing Deployed APIs
You can test your APIs connectiviy and functionality by running the `./test/test_apis.py` script. The script will call each API we have published, and validate the response (you must have bootstraped your account first). Do *note* this does not test the labmda full coverage or functionality, but really servers the pupose of testing apis after they are published, after deployments.

check it out.
```
xxx
```

## CI
The IaC is supporting using AWS `CI` features, the functionality incudles.

- [x] CodePipeline as a wrapper for the IaC pipeline.
- [x] GitHub source (need to have tokens configured), with a hook setup for pushes to the a `develop` branch.
- [x] CodeBuild to package build & package the 'lambads' and the `IaC` foundational components.
- [x] Deploy stage to create/update the CloudFormation templates.

You can provison this pipeline uisng the `./lib/pipeline-iac/iac_pipeline.yaml` file, if you'd like.

### Contributing
If you get access, and would like to contribute to this, please follow this statergy, to get your code commited.

- [x] From `develop` create a branch `:github_username/:feature_name`
- [x] Once ready up a pull request to `develop`. `DaveVED` will have to review it.
- [x] Once approved AWS CI pipeline will be executed, and you should be able to see your changes at `dev.tastingswithtay.com`.

### How the Foundation works
For this project, we are using 'nested stacks' this allows us to keep one copy for each env, that is clean and simple. The way it works is, we import our common components into the foundation, wihtin the common compoents, we define, key features and group them, such as `networking` or `compute` resources are gouped in common components, that are reusable (we use them for our other fun projects to).

In the `buildspec.yml` you can see that we upload these comon files to a private `s3` file, that the foundation uses, so each new build, a new version will get published, and cloudforamtion will check if any updates need to be made. 
