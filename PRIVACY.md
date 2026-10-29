# Privacy policy: DataXAPI plugin for Dify

This plugin is published by Aurevant LLC, which operates DataXAPI. The full DataXAPI privacy policy is at
<https://dataxapi.com/privacy/> and governs everything the service receives; this page says what the plugin itself
does with data.

## What the plugin sends, and where

- The plugin talks to one service only: the DataXAPI API at `https://api.dataxapi.com`, over HTTPS.
- With each tool call it sends the inputs you or your agent gave that tool (an account ID, a post ID or link, search
  terms, a cursor, or the JSON parameters of the "Call any endpoint" tool), your DataXAPI API key in the
  `Authorization` header, the label `X-Source: dify`, and a random idempotency key.
- Checking your credentials sends your key to `GET /v1/account`, which is free.
- The plugin sends nothing else: no conversation history, no files, no data about the people using your Dify app.

## What the plugin stores

- The plugin itself does not store, log or cache any data. Your API key is stored by Dify as a secret credential.
- What DataXAPI keeps is described in its privacy policy: the parameters of a call are kept for 30 days and the result
  of a call for 24 hours; records of calls (endpoint, time, outcome, cost) are kept as accounting records.

## Third parties

- DataXAPI passes the parameters and public identifiers a call needs to the data supplier used by that endpoint. It
  never passes your DataXAPI key or your payment details. See "Who receives data" in the DataXAPI privacy policy.
- The data returned is public data from the platforms. Do not put passwords, cookies or private sessions in any input.

## Contact

support@dataxapi.com

---

## 隐私说明（中文）

本插件由运营 DataXAPI 的 Aurevant LLC 发布。完整的 DataXAPI 隐私政策见 <https://dataxapi.com/zh/privacy/>。

- 插件只连一个服务：`https://api.dataxapi.com`（HTTPS）。每次调用发送你或你的 agent 给这个工具的输入（账号 ID、作品 ID 或链接、搜索词、翻页游标，或“调用任意接口”的 JSON 参数）、放在 `Authorization` 请求头里的 DataXAPI Key、`X-Source: dify` 标记和一个随机的幂等键。校验凭证时调用免费的 `GET /v1/account`。
- 插件不发送对话记录、文件或你的 Dify 应用使用者的信息；插件本身不存储、不记录、不缓存任何数据。Key 由 Dify 作为密钥凭证保存。
- DataXAPI 端：调用参数保留 30 天，调用结果保留 24 小时，调用记录（接口、时间、结果、费用）作为账务记录保留。DataXAPI 会把一次调用需要的参数和公开标识交给该接口使用的数据供应方，从不交出你的 Key 或付款信息。
- 联系：support@dataxapi.com
