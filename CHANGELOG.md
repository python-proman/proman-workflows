
Changelog
=========

# ProMan Versioning Changelog

## v0.1.0a6 - (2022-03-16)

### added

|commit|type|description|
| :--- | :--- | :--- |
|94445bdc455b60f24f1b7b06599aec144df7d501|feat|trying out commit messages|
|baa8370da2b91c747c0ae2bb58239403d57626b5|feat|add validation|
|7cdfc51e520a1ace0dd1c2a3818104f25fa1b193|feat|implement gitflow|
|45ca61f7db324f73c21d560ca21b7c65d65d09c0|feat|conentional commit with file versioning|
|6087f737368243ef7afe527558f5d9fe7c0c8359|feat|implemented gitflow strategy prototype|
|3540cbaf43f58740fd4ec468ae3ec674ca285045|feat|implementing entrypoints|
|01b02b866d205ff4197e63b080bc714763b9789f|feat|base layout|
|58fa5fe5355af2b3d1a74aefe452de840f553637|feat|added additional tools|
|2e6737d73ade68b3d5721993b794eb977cd9e354|feat|add workflow plugin system|
|9bd60dc18a6ef0a29f65acc7c1da5a8f27df3c99|feat|add pygit2|
|085b412778cfea0be63f27754bdc4af07213de40|feat|add gitignore overlay|
|da968bd5e7095b7ba8d8868a6168c0e3c290575a|feat|add gpg setup|
|34aad08ed76a205649596bdd261dff9d2c3b8d03|feat|add submodule capablity|

### changed

|commit|type|description|
| :--- | :--- | :--- |
|592b742a4e44eb2c60283297a8bc627ec58d9918|test|Added tests for conventional commits|
|7d8bcd2600663f694cb86c696386bd1f6989c5a8|refactor|change name|
|aceb61b18d375849c2f2c3b0202987f6d4e5693a|build|fix compendium version|
|787d9b3708fe99446d8401f66bbb8fd3f5021864|refactor|simplify release state|
|cb336ac88820bc2caa2c8a39dceba3a5bcbded11|refactor|fixing layout|
|818f2160172566bcae44f2c245b9443138b84f9c|refactor|switching to task runner|
|bcc84ea3e42fef7190bb6fa05cd11da7b5e51f4d|refactor|separate versioning|
|de664d63179674c333382093dba2103f6d6be2fc|ci|add pipeline|
|b4744d74c7932112c125de47eeb4eb6c720f16dc|refactor|structure project|
|3ae611dc6947932a1f85289d8649eb85c20d41bf|docs|working implementation|
|797db516b561ad387657cad1302638d1676a6e76|style|update types|
|bf99a4e08c57b0d0e2c25dcece25410012d9415d|ci|checking pipeline|
|9917bbf741a32bb02279ef89ce29ca85b664437a|test|add gpg test|
|bf02f08c9e6bcbfc907e10a9f647a7e992ed7fd4|refactor|switch to executor for tasks|
|0cbb6129a1273accad2d353eb19b64f4e8bdaf74|refactor|add all gitignore for license|
|00afbf619f19c3e916ca98363154dbacbbaafa42|style|fix headers|
|f5ad1bb9b9f7e20c3b2996baa19d7c74118994f6|build|replace flit with twine|
|40d1bcd7adab2531cb7f00dd0270ada0cb6a0b41|refactor|fix security findings|
|e0ac7fa844d3814c9f81561ce66d59b149d395d3|refactor|changed to protools|
|8507eff794f92bcf68cda7a3a665536577af0855|refactor|simplify plugin namespace|
|378271d91599f4e52867a5a64211138ee3fca39b|refactor|setup stlc layout|
|9693901ce396b33de5238594d84bacd7320d6645|refactor|cleanup|
|d1e04cf03ebc53a0c0d31e21c59c6002930ae0c5|refactor|wire together the flows|
|401d2de1aa8986d214bdba48830062585893d943|refactor|setup each workflow tasks|
|6402642b9bc26855cdd13320504a6a9dd563455b|refactor|use src layout|
|1f0827c237aeedd706bc15be58c776cb50218ccd|build|bump version|
|5541d7ace4261a3cf65a553803ac6d15d63b72e4|refactor|complete adding workflow stubs|
|16a4e0033f900f504088d2334dfcba9d6f398af1|build|bump version|
|e0d819a505a2c3ebd8136bb3230cf6118b0fd2eb|docs|update the project readme|
|bc2f819d31765fd296698e64546630edd540fb81|docs|update readme|
|a66a396ffe14c9c90ed0bb901ee4a79a5b72aab5|ci|apply 0.1.0a4 updates|
|83e21d622eb96cef59e4f8273c71a48e50521ac4|ci|rewire pipelines|
|e4ab36e22a64433c4bad25028dc72ca024dcc964|ci|rewire pipelines|
|4f1fb85a264a5af68b8f0b2ee4c31f2c6ffe06e1|build|handle cached property backport|
|5cd547d76eff3e8cb06ea6f98b91f93aeda74b5f|build|resolvve python36 pygit issue|
|6673f401890d3b22c3f0ae7fc3318eff2357f424|build|resolvve python36 pygit issue|
|c966204aa723a3f31c04b8e52eda533c9f4ca9b2|refactor|resolve config issue|
|1a5ac2720dd4d008c4f00da5bdd0b1e7fa2c4c5a|ci|fix calls|
|beb6d7ea7114b7d0e81a79dda106eacd7d454a0e|docs|resolve 3.6 deps for mkdocs|
|cf1f4e783ce8649a0c11bd60806c818e9f450792|build|remove 3.6 support|
|2dd0ac12daf8acb14f45d257a09e74b1cace72e9|ci|resolve python 3.10 version|
|881ad9693349584ff6d2e100410ba954b4aa7f71|build|troubleshooting 3.10|
|3a158ae6d93cc999ea6d26498327cb62a6cd37cb|build|troubleshooting 3.7 cached-property|
|efe661201a528b3807a4d023ca6cf604c7a7d2f1|build|troubleshooting tests|
|b2593701d4fa8c4a97aaec3233ff57a5b0676441|docs|troubleshooting tests|
|e5ee891b2dd5378a8aca5c4c77c4220d6322d116|docs|fix builds|
|5f22266932fbe944bddb136cc1f3b10be776013c|docs|fix builds|
|12fcc43d192ad2809bc95c3e9218df78175a8850|docs|coverage|
|d3dc4a248be472b849d415c28698245911068a9f|docs|update readme|
|7db279bfa0379bf21eeb7eebfa5005b4f7956cce|ci|disable mac/win pipelines|
|931c89e25754447da8c367019e28d32a60c2f428|ci|pull changes|
|2d5f4ab4a6dd5ba0fc2882b3b8b9b0b568ac41e9|ci|apply 0.1.0a5 updates|
|751641003d77b19b690a8f24430a1ca513eb3f42|build|remove restrictive jinja deps|
|0a04ce8fecb598ab96a11b7eea118d8e27a51b75|build|update versioning tools|
|13a03a4b3b86c2246a44763369a60fe0d91ad99f|ci|apply 0.1.0a6 updates|

### fixed

|commit|type|description|
| :--- | :--- | :--- |
|667afdccd0d3676c27de3312ce763a0e17a64a0a|fix|stevedore tasks|

### misc

|commit|type|description|
| :--- | :--- | :--- |
|fa1c81d57acbcfc078a9a35cf6e153d4f8fe91be|None|Initial project layout|
|db05eab10a33aece76065f8c228a210316d20bcb|None|Changed project name|
|0346f2b7ab74c74a11668a03b6e8fcfa660356c3|None|Troubleshooting argufy|
|88fa1cd7b8606350ff3d2bf70de7a6f55cfc539c|None|Implemented basic git hooks|
|4ec5841af02d5523d57f04778549bc8af4e09432|None|Added remove for hooks|
|9b1dfaca4efa8a39c2c8322e589dc4f72780394f|None|prototyping some ideas|
|c9fdc882075332ae9480a974139bfa27d7370448|None|Fixed parsing separation|
|fe74c52fad186d86fd57792aed4b1e9287536903|None|Implemented title and body parser|
|f8cf7226743cd8c58da985a106056caeeb4ee061|None|Updates|
|48ac735417aff48c74f7f5f755d3039adb177bd3|None|Merge branch 'master' of github.com:kuwv/python-git-tools|
|c06dec26c20d17d5efa3b3bddbe88244c011d4d7|None|fixed trailer names|
|64b352beca82bb60a835c30b1d3644c54d203235|None|test|
|ee2e59e2932c3df73fc38dbbac9fca71d129634f|None|Update README.md|
|f6b0d739b4da0cb3094aae988d43405c2fda0ab3|None|Update README.md|
|fa98caf515bc12220d8d270b4bcf6ae7c00a3aa9|chore|cleanup|
|0aa630174e1071b3ee418b00190f286cb122b055|None|updated argufy|
|69eeca7d6aa14085430f951cde990ccc731760b7|chore|pygit2|
|c61aab1f5a9f34ccc82b45faa60fbb0d90a17848|chore|reverted name change due to conflict|
