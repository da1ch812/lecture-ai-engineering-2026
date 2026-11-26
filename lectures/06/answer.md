# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：[glossary_search_glossary]
- STEP 2 の [tool call]：[tool call]   glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：以下のように2段階で実行された。
  - [tool call]   aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'})
  - [tool call]   aws_aws___search_documentation({'search_phrase': 'Using versioning in S3 buckets', 'topics': ['general']})
- 気づき・疑問：STEP4の後（≒AWSの外部サーバを追加後）、改めてSTEP3を実行したところ、tool callの挙動が以下のように2段階に変わり、toolの追加によりLLMが動的に判断をしていることがわかったが、呼び出されたtoolはglossaryからであり、追加されたtoolだけが選ばれるわけではなく、望まない挙動をする可能性もある。（今回は、URL先の要約を求めたにもかかわらず、glossaryのツールとして、MCPの説明及び関係回の紹介をしてしまった。）そのため、不要なツールはオフにするような管理も必要になると思料される。
  - [tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
  - [tool call]   glossary_search_glossary({'query': 'MCP'})

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
