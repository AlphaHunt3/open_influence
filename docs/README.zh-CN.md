<p align="center"><img src="../assets/hero.svg" alt="Influence MCP — X、币安广场和YouTube影响力数据" width="100%"></p>

# Influence MCP

**让 AI Agent 知道 AI 和 Web3 领域谁值得关注。**

覆盖 **X、币安广场、YouTube**：查影响力排名、筛选创作者、看领域能力，区分排名上涨、网络关注与真实粉丝增长。

本仓库提供 stdio MCP 服务、异步 Python SDK、CLI 和 Agent Skill。也可以直接连接 [mcp.xhunt.ai](https://mcp.xhunt.ai) 的远程 MCP，无需安装本地客户端。

[English](../README.md) · [客户端配置](clients.md) · [完整工具清单](tools.md) · [使用案例](recipes.md)

## 一分钟接入

到 [账号页](https://mcp.xhunt.ai/account) 用 X 或已验证的 Gmail 登录，创建个人 API key。登录和付款入口需要服务端已部署登录计费版本并配置对应提供商。

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
| 找 AI / Web3 影响力账号 | X 的两类sector × global/en/cn池，各支持前200 |
| 看本周排名上升 | X Weekly rank-gain KOLs，衡量排名上升名次 |
| 看谁得到KOL网络新关注 | X Weekly Trends KOLs，目前Web3 cn/en |
| 筛币安广场创作者 | 前200影响力、账号资料、85分以上领域能力 |
| 看币安广场粉丝增长 | 当前影响力前1000，按7天粉丝净增排序；需已积累基线 |
| 找YouTube创作者 | AI和Web3各前200周榜，保留订阅数、评分及数据周次 |
| 查看擅长领域 | X和币安广场已发布的领域能力，只返回85分及以上 |

X另提供每个handle的六组排名与项目排名、global/cn各Top10 Smart Followers、当前资料与已记录的资料历史、四向关注/取关事件。六组人数支持已完成排名批次的真实去重账号数（含项目），需部署配置快照发布器；缺失或过期时仍为空。国际池不等于严格英语，分类未知时保留空值。Social是有限监测记录，取关约覆盖最近一小时，limit是每种事件的上限，费用最多4×limit；Smart Followers按两组实际返回人数收费，最多20。资料历史每个handle收1credit，不声称覆盖终身。

Following KOLs完整名单、原始timeline/推文搜索、跨平台身份匹配仍未提供。灵魂指数、灵魂榜和能力榜暂不公开。2026-10-29线上已部署个人账户和额度，X登录已配置，Gmail与Pro支付仍未启用，Pro Top500服务端和客户端已实现待部署，kol钱包身份与Influence权益仍待绑定。

## 本地客户端

Python3.10+，安装uv后，在仓库目录执行：

```bash
uv sync --locked
export XHUNT_API_KEY="YOUR_XHUNT_API_KEY"

uv run influence-client capabilities             # 免费，无需key
uv run influence-client usage                    # 免费，需登录计费版服务
uv run influence-client x --sector web3 --region cn --limit 10
uv run influence-client youtube --sector ai --limit 10
uv run influence-client square --limit 10
uv run influence-client serve                    # stdio MCP
```

本地列表默认10条，上限200。远程MCP沿用服务端默认200，建议明确指定limit=10。本地增加`get_usage`工具，调用REST额度接口；远程MCP目前没有同名工具。

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

- 按成功返回人数计费：每人/频道1credit；资料或能力模型每次1credit；空结果、错误、capabilities及usage免费。
- 免费月额度1,000–8,000，取决于XHunt排名；Gmail为1,000。Pro39美元/月，30,000credit；机构可申请额外免费额度。
- 日上限为月额度的四分之一，按UTC自然日/月重置；同一账号多个key、REST/MCP共用额度和每endpoint每分钟100次的限流。
- 本地响应`_client.credits_charged`来自服务端实际扣费头；缺少计费头时为null，不会说成免费。客户端不自动重试、不隐藏多次调用、不购买额度。
- 网络超时可能已经消耗credit。`quota_exceeded`要等额度恢复或调整计划，`rate_limited`才是短时间限流。

查10人榜单，再查其中3人的资料和能力，最多16credit。按需取少量，比每次拉前200更适合Agent研究。

X的`en`是国际来源池，并非严格英文筛选。新进入榜单包含重新上榜，不代表首次发现。币安广场周榜从2026-10-28积累历史，无基线时返回`insufficient_history`。YouTube的Web3对应Crypto，按已完成周报发布。不同平台分数不直接合并。

以上计费规则以登录计费分支实现为准；正式服务是否已启用，需看部署及配置。真实数据的新鲜度以响应时间字段为准。

客户端默认只向`mcp.xhunt.ai`发送只读请求，不遥测、不写入凭证、不执行返回内容里的命令。MIT许可覆盖客户端代码，不表示开放托管数据或免费无限调用。

觉得有用欢迎Star，也欢迎提交案例、客户端配置与翻译。

币安周增长榜新增 `square-weekly --region cn`（或 `en`），在全站影响力Top1000候选中先筛语言再截取。需要服务端部署2026-10-29新增的region支持；先检查capabilities中的weekly_regions，旧服务可能忽略此参数。历史不足时仍无结果。

Circle：`uv run influence-client circle cz_binance --days 7`，或MCP `get_kol_circle`。默认7天、可选1至30天，返回最多10个双向回复/引用/转推账号，每个方向至少有一次互动；按双方唯一互动帖总数、较小方向计数、账号ID排序。按实际人数收费，最多10 credits。仅覆盖已记录帖子，目标缺失返回partial，不推断完整X活跃情况；查询超限会失败，不返回截断榜单。需要新版服务及显式只读源配置；目前生产部署另行安排。

Pro：`uv run influence-client pro --platform x --sector ai --region cn --limit 10`，或MCP `get_pro_leaderboard`。需要有效Pro，最多500条，每个实际返回账号1 credit；本地默认10、服务端默认500。普通接口仍最多100。币安/YouTube不提供区域池。YouTube W44有效池为AI727、Web3429，AI可取500，Web3明确返回insufficient_coverage；不凑数。两端显式钱包绑定和共享Pro权益已实现并通过隔离测试；生产配置和上线仍待完成。

新增wheel独立安装检查：验证CLI入口、Python SDK及真实stdio MCP初始化/工具发现/调用，不接受editable源码导入。CI离线模式不请求数据；隔离真实接口模式还核对三平台、免费账号拒绝Pro及实际额度账本。详见[验证步骤](verification.md#wheel-installation)。
