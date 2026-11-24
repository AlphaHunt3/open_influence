<p align="center"><img src="../assets/hero.svg" alt="Influence MCP — X、币安广场和YouTube影响力数据" width="100%"></p>

# Influence MCP

**让 AI Agent 知道 AI 和 Web3 领域谁值得关注。**

覆盖 **X、币安广场、YouTube**：查影响力排名、筛选创作者、看领域能力，区分排名上涨、网络关注与真实粉丝增长。

本仓库提供 stdio MCP 服务、异步 Python SDK、CLI 和 Agent Skill。也可以直接连接 [mcp.xhunt.ai](https://mcp.xhunt.ai) 的远程 MCP，无需安装本地客户端。

[English](../README.md) · [客户端配置](clients.md) · [完整工具清单](tools.md) · [使用案例](recipes.md)

## 一分钟接入

到 [账号页](https://mcp.xhunt.ai/account) 用 X 或已验证的 @gmail.com Google 账号登录，创建个人 API key。付款方式和价格以账户页当前展示为准。

Claude Code 直接接入：

```bash
claude mcp add --transport http influence https://mcp.xhunt.ai/mcp \
  --header "Authorization: Bearer YOUR_XHUNT_API_KEY"
```

在本地替换 key，然后问：

> 分别找出 X 和 YouTube 上排名前10的 AI 创作者，保留平台、数据时间和可用指标，解释为什么不能直接比较两边分数。

或将下面的话交给你的 Agent：

```text
连接 https://mcp.xhunt.ai/mcp，使用我在本地配置的私密API key。
先查询capabilities。每次列表最多取10条，除非我要求更多。
保留数据时间，明确趋势究竟是排名、网络新增关注还是粉丝净增。
不要在回复或Git文件中写入我的API key。
```

Cursor、VS Code、Claude Desktop、Windsurf 及本地 stdio 配置见[接入指南](clients.md)。

## 能做什么

| 场景 | 已实现能力 |
| --- | --- |
| 找 AI / Web3 影响力账号 | X 的两类sector × global/en/cn池，免费最多100位，Pro最多500位 |
| 看本周排名上升 | X Weekly rank-gain KOLs，衡量排名上升名次 |
| 看谁得到KOL网络新关注 | X Weekly Trends KOLs，AI/Web3 cn/en |
| 筛币安广场创作者 | 免费前100／Pro前500影响力、账号资料、85分以上领域能力 |
| 看币安广场粉丝增长 | 当前影响力前1000，按7天粉丝净增排序；需已积累基线 |
| 找YouTube创作者 | AI和Web3各免费前100／Pro前500周榜，保留订阅数、评分及数据周次 |
| 查看擅长领域 | X和币安广场已发布的领域能力，只返回85分及以上 |

X另提供每个handle的六组排名与项目排名、全球/中文/Top100三组聪明粉丝、当前资料、资料历史及四向关注/取关事件。人数缺失或过期时保持空值并说明状态，国际池不等于严格英语。聪明粉丝、Social、Circle和资料历史均按整页成功且非空的查询收1积分，包含所有分组和记录，不按人数、事件或快照条数累计；空结果、处理中和失败不扣分。各分组免费最多10条、Pro最多40条，实际数量受来源覆盖限制。Free取关/被取关只可查看72小时以前的记录，Pro没有套餐时间截断；资料历史不声称覆盖终身。

Following KOLs完整名单、原始timeline/推文搜索、跨平台身份匹配仍未提供。不提供独立的灵魂指数接口、灵魂榜和能力榜；X 主榜仍可能附带已发布的 Soul 分数。截至2026-11-23，X/Google登录、两站共享Pro与永久积分充值已实现并部署；完整真人授权、实际付款到账和银行卡续费仍需单独验收。当前登录无需钱包。Google要求已验证的@gmail.com账号。

## 本地客户端

Python3.10+，安装uv后，在仓库目录执行：

```bash
uv sync --locked
export XHUNT_API_KEY="YOUR_XHUNT_API_KEY"

uv run influence-client capabilities             # 免费，无需key
uv run influence-client usage                    # 免费；需要个人 API key
uv run influence-client x --sector web3 --region cn --limit 10
uv run influence-client youtube --sector ai --limit 10
uv run influence-client square --limit 10
uv run influence-client serve                    # stdio MCP
```

CLI列表默认10条；SDK/MCP主榜默认10条。普通主榜接口对两个套餐均最多返回100位，Pro独立入口最多500位；详情、周榜与热门列表每组免费最多10条、Pro最多40条。SDK/MCP省略这些列表的limit时使用套餐上限；建议先明确指定limit=10。本地与远程MCP均提供免费的`get_usage`，本地版本调用REST额度接口。

Python SDK：

```python
import asyncio
from influence_client import InfluenceClient

async def main():
    async with InfluenceClient() as client:
        result = await client.youtube_leaderboard(sector="ai", limit=5)
        print(result["items"])
        print(result["meta"], result["_client"])

asyncio.run(main())
```

## 费用与口径

- KOL排行榜及热门/趋势KOL榜为0credit；每日热门/飙升推文API/MCP每次成功非空请求扣1分，网页浏览免费（Pro Top500仍需有效订阅）；聪明粉丝、Social、Circle和资料历史每次成功且非空的整页查询收1credit，包含全部分组；资料、排名矩阵或能力模型每次成功返回账号收1credit；空结果、处理中、错误、capabilities及usage免费。
- 免费月额度1,000–8,000，取决于XHunt排名；Google为1,000。Pro为30,000积分/月；月付$19.99（原价$29.90，约33%优惠），季付$45/三个月；季付每月30,000积分，连续三个月，不一次性发90,000；加密货币单次购买、银行卡按所选周期自动续费；已有合同保留原价；机构可申请额外免费额度。
- 套餐日上限为套餐月额度的四分之一，永久充值积分不受此日上限限制，按UTC自然日/月重置；同一账号多个key、网页、REST/MCP共用额度及限流。Free全局120/分钟、5000/日，每接口60/分钟、100/日；Pro全局300/分钟、30000/日，每接口60/分钟、500/日。
- 本地响应`_client.credits_charged`来自服务端实际扣费头；缺少计费头时为null，不会说成免费。客户端不自动重试、不隐藏多次调用、不购买额度。
- 网络超时可能已经消耗credit。`quota_exceeded`要等额度恢复或调整计划，`rate_limited`表示请求次数限额，可能是分钟或每日上限，请按Retry-After等待。

查10人榜单，再查其中3人的资料和能力，最多6credit。按需取少量，比每次拉完整榜单更适合Agent研究。

X的`en`是国际来源池，并非严格英文筛选。新进入榜单包含重新上榜，不代表首次发现。币安广场周榜从2026-10-28积累历史，无基线时返回`insufficient_history`。YouTube的Web3对应Crypto，按已完成周报发布。不同平台分数不直接合并。

以上规则与2026-11-24公开服务元数据核对；后续以capabilities和实际计费头为准。真实数据的新鲜度请查看meta.freshness及来源时间；served_at只是响应时间，snapshot_at为空时表示未知，不能当成最新。

客户端默认只向`mcp.xhunt.ai`发送只读请求，不遥测、不写入凭证、不执行返回内容里的命令。MIT许可覆盖客户端代码，不表示开放托管数据或免费无限调用。

觉得有用欢迎Star，也欢迎提交案例、客户端配置与翻译。

币安周增长榜新增 `square-weekly --region cn`（或 `en`），在全站影响力Top1000候选中先筛语言再截取。先检查capabilities中的weekly_regions；客户端会拒绝未确认对应语言的非空结果，避免旧服务忽略参数。历史不足时仍无结果。

Circle：`uv run influence-client circle cz_binance --days 7 --limit 10`，或MCP `get_kol_circle`。默认7天、可选1至30天；每组免费最多10位、Pro最多40位，各方向至少有一次直接回复/引用/转推。按双方唯一互动帖总数、较小方向计数、账号ID排序，整页成功且非空时扣1积分，不按伙伴数累计。覆盖不完整时保留partial；SQL超时可返回不扣分的pending和建议重试时间，客户端不会自动轮询。缓存数据保留原时间，命中缓存仍正常计费；其他故障不伪装为空榜成功。

Pro：`uv run influence-client pro --platform x --sector ai --region cn --limit 10`，或MCP `get_pro_leaderboard`。需要有效Pro，最多500条，榜单查询不扣credits；本地默认10、服务端默认500。普通接口仍最多100。币安/YouTube不提供区域池。当前数据量、周次及不足说明以响应元数据为准，不凑数。两站使用X/Google共享账号权益，不需要钱包绑定。

新增wheel独立安装检查：验证CLI入口、Python SDK及真实stdio MCP初始化/工具发现/调用，不接受editable源码导入。CI离线模式不请求数据；隔离真实接口模式还核对三平台、免费账号拒绝Pro及实际额度账本。详见[验证步骤](verification.md#wheel-installation)。

永久积分充值：Free/Pro均可买全部四档：$5→4,000、$10→10,000、$50→60,000、$100→150,000。加密货币与银行卡充值均单次付款，积分永不过期，不升级套餐、不延长Pro。先用套餐当日可用额度，再扣充值积分；充值余额不受套餐日额度限制，接口限流仍适用。到账记录和刷新入口在账户页，客户端不代购。详见[账户与计费](billing.md)。

## 热门KOL与推文

CLI、Python和MCP均支持今日/本周热门KOL、每日热门推文、每日飙升推文；AI和Web3均有中文/国际池。每周Smart Follower关注榜也支持AI。国际池不保证纯英文。

```bash
uv run influence-client hot-kols --sector ai --region cn --days 7 --limit 5
uv run influence-client hot-tweets --sector web3 --region en --limit 5
uv run influence-client rising-tweets --sector ai --region cn --limit 5
uv run influence-client weekly --sector ai --region cn --limit 5
```

热门KOL榜不扣分；热门/飙升推文API每次成功非空扣1分，条数不影响价格。所有列表命令均支持`--limit`，包括聪明粉丝、互动圈、资料历史和能力模型的推文依据。CLI默认10条；SDK/MCP省略详情列表上限时使用当前套餐上限，免费每组10条，Pro每组40条，来源不足时可能更少。完整对应关系见[工具参考](tools.md)。

使用X账号购买Pro可获赠等长插件VIP，每次购买继续累加原有插件时长。插件单独购买不授予网站/API Pro或积分；Google登录和积分充值不赠送，取消本站续费不收回已赠送插件时长。

涨聪明粉周榜按近7天首次观察到的有效新增聪明粉人数降序排列，不按普通粉丝总数或加权热度排序；每小时刷新，六小时过期后按请求重新生成。观察时间不是X实际关注时间。Web3按关注者来源池分组；AI另外要求被关注者在相应AI候选池内，并按其语言分类筛选。Smart Followers按每组有效上限请求来源接口（Free最多10、Pro最多40）；合格账号不足时按实际人数返回，请查看total_count、available_count和source_limited。

服务端和本地MCP均提供免费的get_usage作为连接检查。账户页可看Key最近使用时间及近30天已记录的调用。客户端保留_client.rate_limits和_client.request_id，便于按限流余量退避和核对调用记录。鉴权错误区分Key缺失、无效、已撤销及请求头错误；MCP使用API Key，不提供OAuth授权。
