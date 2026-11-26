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

- 取り組んだレベル：発展
- やったこと：普段利用しているコーディングエージェントであるContinue（VS Code拡張機能）へのMCPサーバの設定方法を公式ドキュメントで調査し、演習で使った mcp_servers.jsonと比較した。
  - 調査日：2026-11-26
  - 公式URL：https://docs.continue.dev/
  - MCP servers：https://docs.continue.dev/customize/mcp-tools
  - リファレンス（config.yaml / mcpServers）：https://docs.continue.dev/reference#mcpservers
  - 関連ガイド（構成・スコープ）：https://docs.continue.dev/guides/configuring-models-rules-tools
- 結果：
  - 設定を書く場所・形式：演習ではapp/mcp_servers.jsonに"mcpServers"オブジェクト（サーバー名をキーとする辞書）で記述するのに対し、Continueの現行リファレンスでは複数の要素をまとめて定義できるconfig.yamlの中のmcpServersに配列として記述する形式になっている（以前はconfig.jsonであったが、現在は非推奨扱い）。
  - コマンドで起動する書き方：
    - 設定のcommand：演習は"command"と"args"（uvやuvxなど）を指定するシンプルな構成であるのに対し、ContinueのmcpServersではcommand・argsに加えてenv（環境変数）やcwd（作業ディレクトリ）、connectionTimeoutなどの実行環境オプションを指定できる。
    - 起動のcommand：演習ではuv run python -m app.mcp_agent --trace "..."のようにCLIコマンドで質問やURLなどのコンテキストを直接渡して実行するが、Continueでは設定ファイル（config.yaml）でMCPサーバーやコンテキスト・ルールを定義しつつ、実際のプロンプト送信やコンテキスト付与は一般的にVS Code上のUI・操作を通じて行う点が異なる。
  - URLで接続する書き方：演習は"url"にエンドポイントURLを指定する形であるのに対し、Continue側でもリモート接続向けのrequestOptionsなどのオプション項目が用意されている。
  - 有効になる範囲：演習はapp/mcp_servers.jsonを読み込む演習エージェントの範囲で有効になる。Continueでは設定の置き場所や仕組みによって適用範囲が分かれており、グローバル設定（~/.continue/config.yaml等）は特定のプロジェクトに閉じず全ワークスペース（どのプロジェクトを開いていても共通）で有効になる一方、ワークスペース向けの設定（.continue/mcpServers等）は対象プロジェクトで作業する際に適用される。
- 気づき・疑問：
  - 演習のJSONではキー名でサーバーを識別していたが、Continueのconfig.yamlでは配列要素ごとにnameを持たせつつcwdやenvを添えられるため、複数環境やローカルツールを扱う際の柔軟性が高いと感じた。
  - 一方で、外部コマンドやリモートURLを簡単に追加できる分、提供元の信頼性や環境変数・通信先のリスク管理をどう担保するかは意識したいポイントだと感じた。