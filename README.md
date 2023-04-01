# tastingswithtay-iac
Resources supporting the management and creation of the infrasture for `tastingswithtay`, which is a `react` frontend service, with a `serverless` backend spun up to support my [wife](https://www.linkedin.com/search/results/all/?fetchDeterministicClustersOnly=true&heroEntityKey=urn%3Ali%3Afsd_profile%3AACoAAA2cmMIBoJJcTrc_KMA9KfnvpC_o09K2LhI&keywords=taylor%20dennis%20cfp%C2%AE&origin=RICH_QUERY_SUGGESTION&position=0&searchId=7814197b-183e-411a-8544-ddf606477752&sid=T%3Bg). You can view her cooking recipies, stay up to date with our chickens, or see what we're currenlty going in our garden to be used in her recipes. Check it out [here](http://tastingswithtay.com/)!


This `IaC` could also be forked, and used to support any `3 tier` application you wanted to host on `AWS`.


## CI
The IaC is supporting using AWS `CI` features, the functionality incudles.

- [x] CodePipeline as a wrapper for the IaC pipeline.
- [x] GitHub source (need to have tokens configured), with a hook setup for pushes to the a `develop` branch.
- [x] CodeBuild to package build & package the 'lambads' and the `IaC` foundational components.
- [x] Deploy stage to create/update the CloudFormation templates.

You can provison this pipeline uisng the `./lib/pipeline-iac/iac_pipeline.yaml` file, if you'd like.

#### How the Foundation Components work
#### Branching Stratergy
#### Supporting your react pipeline


## Bootstraping the Data
When the infastruce is first spun up, you should bootstrap the `dynamdodb` database, and `s3` asset bucket with the intial data needed to support basic functionality. The can be done using the `init_dump.py` script. This will.

- [x] Populate the s3 asset bucekt with the images supporting the initial recipes.
- [x] Populate the dynamodb with the intial content (recipes) and the metadata to support those.

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
xxx
```

## Testing Deployed APIs
You can test your APIs connectiviy and functionality by running the `./test/test_apis.py` script. The script will call each API we have published, and validate the response (you must have bootstraped your account first). Do *note* this does not test the labmda full coverage or functionality, but really servers the pupose of testing apis after they are published, after deployments.