# 部署到 han-yy 的 GitHub Pages

这是可直接发布的静态网站，无需安装依赖或运行构建。建议使用独立仓库 `dexterity-atlas`。

部署完成后的默认网址：**https://han-yy.github.io/dexterity-atlas/**。这是预期地址，打包完成不代表已经上线；实际地址以仓库 Settings → Pages 显示为准。若账号设置了自定义域名，GitHub 可能使用该域名。

## 第一次发布：全部通过网页操作

1. 下载并解压 `dexterity-atlas-github-pages.zip`。解压后的内容应直接包含 `index.html`、`app.js`、`data.js`、`hand.js`、`style.css`，以及 `assets`、`vendor`、`research`、`quality` 等文件夹。
2. 登录 `han-yy`，打开 https://github.com/new ，Owner 选择 `han-yy`，Repository name 填 `dexterity-atlas`，选 **Public**，打开 **Add README**，点击 **Create repository**。如果该仓库已经存在且存有其他内容，先换一个新仓库名，避免覆盖。
3. 在新仓库点 **Add file → Upload files**。将解压后的所有文件和文件夹拖入上传区，点击 **Commit changes**，提交到 `main`。上传的是解压后的内容，不是 ZIP，也不要再套一层 `dexterity-atlas` 文件夹。仓库首页应直接看到 `index.html`。
4. 包含空文件 `.nojekyll`；如果文件管理器隐藏它导致漏传，可在 GitHub 点 **Add file → Create new file**，文件名填 `.nojekyll`，内容留空并提交。
5. 打开 https://github.com/han-yy/dexterity-atlas/settings/pages ，在 **Build and deployment** 下将 **Source** 设为 **Deploy from a branch**，Branch 选 **main**，文件夹选 **/(root)**，点 **Save**。
6. 等待发布完成，首次发布可能需要几分钟，官方文档提示最多可达 10 分钟。刷新 Pages 页面，点击 **Visit site**。也可以在 **Actions** 查看部署是否成功。

## 发布后检查

- 打开“动作库”，应显示 231 个动作；可筛选、搜索并打开动作详情。
- 在详情查看来源链接、原始图示或官方视频；“3D 关节示意”筛选应返回 18 个动作。
- 查看“元动作”的 37 项与“道具清单”的 79 项。
- 向采集清单添加动作，尝试导出 CSV 或 JSON。
- “参考来源”有 24 项；直接来源、改编任务和自行扩展都有独立标记。

## 后续更新

将修改后的对应文件上传到同一仓库并提交到 `main`，GitHub 会自动重新发布。无需再次更改 Pages 设置。采集清单保存在使用者自己的浏览器中，不会跨设备同步。

## 常见问题

- **404**：确认 Pages 设置为 `main` + `/(root)`，并确认 `index.html` 位于仓库根目录；然后检查 Actions 是否成功、等待发布完成。
- **页面没有样式或图片**：检查是否漏传 `style.css`、`assets/`、`vendor/` 等，保留原有文件夹结构。此站使用相对路径，支持 GitHub 项目子路径。
- **视频不能播放**：视频由原研究项目托管，需要访问外部网络；动作详情提供原始来源入口。图示和 3D 程序随包附带。
- **3D 显示方式**：优先使用 WebGL；不可用时使用同一场景的 CPU 投影。模型是关节运动示意，未验证碰撞、接触力或物理可行性。
- **已有个人主页**：独立项目仓库不需要改动 `han-yy.github.io` 仓库。

## 官方说明

- [配置发布来源](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [创建 GitHub Pages 网站](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

GitHub Free 支持公共仓库的 Pages。站点保留原始图示和视频的来源署名；原素材版权仍归各权利人。111 个自行扩展动作是数采设计建议，不应当作已被论文逐项验证的实验任务。
