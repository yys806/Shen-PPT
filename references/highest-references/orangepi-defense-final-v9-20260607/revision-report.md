# Shen-PPT 产品化修订报告

## 输出文件

- PPTX: `D:\禹尧珅\人工智能知识库\大三下\综B\大作业\答辩PPT\OrangePi云台目标跟踪系统_课程答辩新版_精修版9_产品化版.pptx`
- Contact sheet: `D:\禹尧珅\人工智能知识库\大三下\综B\大作业\答辩PPT\productized-review\contact-sheet-productized-v9.png`
- Slide cards: `slide-cards-productized.json`
- Asset manifest: `asset-manifest-productized.json`
- QA record: `qa-productized-v9.json`

## QA 摘要

- Slide count: 22
- Slides with notes: 22
- Slides with animations: 0
- Slides with transitions: 0
- Tracked asset rows: 12

## 可见修订

- 第 15 页证据说明改为面向老师的证据表达，删除内部讲解口吻
- 第 18 页曲线解读长句拆分，避免说明挤在一起
- 第 19 页实验判断拆分 C++ wheel 与 OpenCV 的关系，避免一句话黏连
- 所有页面写入私有 PowerPoint 备注，不显示在页面上
- 所有图片对象补充可追踪 AlternativeText，指向资产清单
- 全篇保持无动画、无切换

## Slide Card 摘要

### Slide 01
- Purpose: 建立课程答辩主题和项目总体印象
- Claim: 本项目围绕 OrangePi 板端目标跟踪云台完成软硬件一体化实现
- Evidence: README 指标摘要与报告结果表
- Layout: cover
- QA risk: 封面指标要与报告保持一致

### Slide 02
- Purpose: 给老师建立答辩路线
- Claim: 全篇按背景要求、硬件网络、软件控制、运行证据、结果加分、总结优化展开
- Evidence: 最终 PPT 章节结构
- Layout: directory
- QA risk: 目录标题必须和导航标签一致

### Slide 03
- Purpose: 进入第一章并概括要点
- Claim: 选题由课程要求和现场演示稳定性共同决定
- Evidence: 大作业要求 docx、报告项目背景
- Layout: section divider
- QA risk: 章节页不要堆过多正文

### Slide 04
- Purpose: 解释项目为什么做和做什么
- Claim: 云台跟踪任务能够覆盖开发板、视觉、外设控制和网络调试等课程核心要求
- Evidence: 大作业要求与报告第 1 章
- Layout: comparison matrix
- QA risk: 左侧正文较多，需要保持老师可读

### Slide 05
- Purpose: 逐项对照课程要求和完成情况
- Claim: 主线任务和加分项都有对应证据支撑
- Evidence: 要求文件、终端截图、报告加分实验
- Layout: comparison matrix
- QA risk: 六项内容密集，颜色和状态标记必须统一

### Slide 06
- Purpose: 进入硬件网络章节
- Claim: 真实系统由硬件链路、网络链路和调试入口共同保证
- Evidence: 接线图、网络截图、SSH 截图
- Layout: section divider
- QA risk: 章节概括保持简短

### Slide 07
- Purpose: 证明硬件真实接线和外设识别
- Claim: OrangePi、摄像头、PCA9685、舵机和供电链路已经实际连通
- Evidence: wiring_real、step02_hardware_check、I2C scan
- Layout: evidence split
- QA risk: 实物图和终端图要完整显示

### Slide 08
- Purpose: 证明网络共享和远程调试链路
- Claim: 电脑和 OrangePi 通过有线连接与网络共享形成稳定调试链路
- Evidence: ethernet_diagram、network_share_pc、network_board、ssh_connection
- Layout: evidence grid
- QA risk: 多图页需避免图片过小

### Slide 09
- Purpose: 进入软件实现章节
- Claim: 软件实现按采集、检测、控制、网页和驱动逐步打通
- Evidence: README 和 src/orangepi_tracker 模块
- Layout: section divider
- QA risk: 不要把章节页讲成正文页

### Slide 10
- Purpose: 说明代码模块如何协同
- Claim: 摄像头帧经过检测、状态判断和控制器后转为 PWM 输出
- Evidence: camera.py、tracker.py、state_machine.py、control.py、hardware.py
- Layout: process flow
- QA risk: 流程箭头必须清楚

### Slide 11
- Purpose: 展示网页控制台作为演示入口
- Claim: 网页控制台把实时画面、标定、跟踪和急停复位集中到浏览器
- Evidence: step04_web_real、step04_real_terminal
- Layout: evidence split
- QA risk: 网页截图内容需足够大

### Slide 12
- Purpose: 解释视觉检测到控制执行的闭环
- Claim: HSV 分割、形态学处理、候选筛选和控制策略共同提升稳定性
- Evidence: tracker.py、control.py、gimbal_angle_curve、web real screenshot
- Layout: process flow
- QA risk: 流程行和箭头不能拥挤

### Slide 13
- Purpose: 进入运行证据章节
- Claim: 一键脚本和终端截图让系统运行过程可复查
- Evidence: docs/TEST_COMMANDS.md 和终端截图
- Layout: section divider
- QA risk: 章节页文字保持精炼

### Slide 14
- Purpose: 说明脚本化验证顺序
- Claim: 8 个脚本覆盖从环境检查到日志分析的完整验证链路
- Evidence: scripts/run/* 和 TEST_COMMANDS.md
- Layout: process flow
- QA risk: 截图标签需要可读

### Slide 15
- Purpose: 集中展示加分项终端证据
- Claim: C++ wheel、pymp 和 mock 云端上传都有真实终端输出证明
- Evidence: step05_cpp_benchmark、step06_pymp_benchmark、step07_cloud_*
- Layout: evidence grid
- QA risk: 避免出现“这一页”之类内部提示

### Slide 16
- Purpose: 进入结果和加分实验章节
- Claim: 跟踪指标、性能对比和云端上传构成结果评价主体
- Evidence: 报告第 5 章
- Layout: section divider
- QA risk: 章节页避免过度展开

### Slide 17
- Purpose: 展示代表运行核心指标
- Claim: 代表运行可达到 23 FPS 量级并保留误差、找到率和重捕获指标
- Evidence: 报告 20260524_013921 指标表
- Layout: results dominant
- QA risk: 36.80% 找到率需解释为调试过程数据

### Slide 18
- Purpose: 用曲线解释跟踪过程
- Claim: 误差、角度、FPS 和检测状态曲线可以复查运行过程中的稳定性和异常
- Evidence: center_error_curve、gimbal_angle_curve、fps_curve、target_found_curve
- Layout: results dominant
- QA risk: 长句需要分行

### Slide 19
- Purpose: 展示性能加分实验
- Claim: C++ wheel 相比纯 Python 明显加速，同时 OpenCV 仍是最快后端
- Evidence: morphology benchmark table and terminal screenshots
- Layout: comparison matrix
- QA risk: 实验判断文字需要分行

### Slide 20
- Purpose: 进入总结章节
- Claim: 项目主线完成，但识别鲁棒性和云端接口仍有后续空间
- Evidence: README 完成情况和报告总结
- Layout: section divider
- QA risk: 不要再展开新证据

### Slide 21
- Purpose: 总结云端上传和最终完成情况
- Claim: mock 云端上传证明网络加分链路跑通，最终完成项有截图和指标支撑
- Evidence: step07 cloud upload, payload table, report conclusion
- Layout: summary
- QA risk: 总结文字不能泛泛而谈

### Slide 22
- Purpose: 正式结束答辩
- Claim: 以感谢页结束并请求老师批评指正
- Evidence: deck topic and presenter metadata
- Layout: thanks
- QA risk: 保持居中和无框

