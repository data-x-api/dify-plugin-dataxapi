# DataXAPI 社媒与市场数据（Dify 插件）

> 现状：还没有发布。这是本地构建的版本，还没提交到 Dify 插件市场。

源码仓库：<https://github.com/data-x-api/dify-plugin-dataxapi> · 联系：support@dataxapi.com

[DataXAPI](https://dataxapi.com/zh/) 用同一种返回结构给出抖音、小红书、微信公众号、视频号、快手、TikTok、B站等平台的公开数据。这个插件把它接进 Dify 的工作流、Chatflow 和 Agent。

- 不用登录你自己的平台账号，只要一把 DataXAPI API Key。
- 从 DataXAPI 余额按次扣费，调用出错不收费。每个接口的价格以 [dataxapi.com/apis](https://dataxapi.com/zh/apis/) 上的接口页为准；每次结果都写明这次扣了多少（`billing.amount`，美元）。
- 一次调用返回一页。下一页是带 `cursor` 的新调用，单独计费。

## 工具

| 工具 | 返回什么 | 平台 |
|---|---|---|
| 公众号历史文章 | 一个公众号发过的文章，从新到旧 | 微信公众号（`gh_` 开头的原始 ID） |
| 账号作品列表 | 一个账号发过的作品或视频 | 抖音、小红书、视频号、快手、TikTok、B站 |
| 作品评论 | 一条作品、视频或文章下的评论 | 抖音、小红书、视频号、公众号文章、快手、TikTok、B站 |
| 关键词搜索 | 按关键词搜到的公开内容 | 抖音、小红书、视频号、微信搜一搜、快手、TikTok |
| 调用任意接口 | 用接口编号加 JSON 参数调任意一个接口 | [dataxapi.com/apis](https://dataxapi.com/zh/apis/) 上列出的全部接口 |

每个工具返回 JSON：`data`（`items` 列表或单个对象）、`page.next_cursor`、`warnings`、`billing`（`amount`、`balance_after`）和 `request_id`。作品、评论、账号在各平台用同一套字段。

## 安装和配置

1. 在 DataXAPI 控制台创建 Key：<https://dataxapi.com/console/keys/?ref=dify>。免费试用，最多 333 次，不用绑卡。
2. 在 Dify 里安装插件（上架后从插件市场装，或者装本地 `.difypkg` 文件），打开它的工具设置，把 Key（以 `dx_` 开头）填进凭证。
3. Dify 用免费的 `GET /v1/account` 校验 Key，不扣钱。

## 怎么用

- **工作流**：加一个工具节点，比如“账号作品列表”，选平台，把上一个节点的账号 ID 接进来。要多页就按 `page.next_cursor` 循环，每一页是一次收费调用。
- **Agent**：勾上要用的工具。Agent 自己选平台、填 ID；工具说明里写了每一页是一次单独收费的调用。
- “调用任意接口”示例：接口 `douyin.users.get`，参数 `{"id": "MS4w..."}`。每个接口的参数见它在 dataxapi.com/apis 上的页面。

“账号作品列表”各平台填什么：抖音填 `sec_uid`（以 `MS4w` 开头）；小红书填用户 ID 或主页链接；视频号填 `v2_...@finder`；快手填数字用户 ID；TikTok 填不带 `@` 的用户名；B站填 `mid`。

## 网络连接

插件只向 `https://api.dataxapi.com` 发 HTTPS 请求，带 `Authorization: Bearer <key>` 和 `X-Source: dify`（在用量里能单独看到从 Dify 来的调用）。不需要别的网络访问。出错时返回一段文字，写明错误码、扣没扣钱。

## 隐私

见 [PRIVACY.md](../PRIVACY.md) 和 DataXAPI 隐私政策 <https://dataxapi.com/zh/privacy/>。法定主体 Aurevant LLC。

## 本地开发和测试

需要 Python 3.12 和 [uv](https://docs.astral.sh/uv/)。

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt
.venv/bin/python -m pytest
```

测试把所有 HTTP 请求都 mock 掉，不会调用收费接口。

想连一个 Dify 实例试：把 `.env.example` 复制成 `.env`，填上 Dify 插件调试页给的地址和调试 Key，运行 `.venv/bin/python -m main`。

## 打包并提交到 Dify 插件市场

1. 装 Dify 插件命令行（单独的可执行文件，在 [dify-plugin-daemon 的 Releases](https://github.com/langgenius/dify-plugin-daemon/releases) 下载；详见 [Dify 插件文档](https://docs.dify.ai/en/develop-plugin/getting-started/getting-started-dify-plugin)）。
2. 在上一级目录运行 `dify plugin package ./dify-plugin-dataxapi`，把生成的文件改名为 `dataxapi-0.1.0.difypkg`。`.difyignore` 会把测试、虚拟环境和缓存排除在包外。
3. 用 `data-x-api` 这个 GitHub 账号 fork [langgenius/dify-plugins](https://github.com/langgenius/dify-plugins)，只加一个文件 `dataxapi/dataxapi/dataxapi-0.1.0.difypkg`，按仓库模板提 PR。风险等级选 Medium（会把用户给的 ID 和链接发到外部 API）；敏感能力：无。
4. 以后发新版：先改 `manifest.yaml` 里的 `version`，更新 PR 只加新的 `.difypkg`。

## 许可

MIT
