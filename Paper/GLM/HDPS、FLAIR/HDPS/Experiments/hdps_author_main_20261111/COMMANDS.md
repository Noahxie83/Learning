# 启动与恢复

使用训练监控器截图中的启动方式：由服务器 tmux 等待任意一张卡连续空闲 60 秒，利用率不超过 5%，已用显存不超过 1024 MiB，再启动一次。监控器负责选择物理卡，并通过 `CUDA_VISIBLE_DEVICES` 传入 UUID；本脚本沿用这一分配，进程内使用 `cuda:0`。

- Python：`/data2/cy/xzn/envs/hdps_repro/bin/python`
- 工作目录：`/data2/cy/xzn/Code/HDPS`
- 唯一脚本入口：`/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111/start.py`
- 启动参数：留空
- 日志：`/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111/logs/console.log`
- 状态：`/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111/status.json`
- 检查点目录：`/data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111/checkpoints`

入口会补齐离线模型、Torch 权重缓存与 CPU 线程设置；误用系统 Python 时先切换到已准备的环境。批处理在同一进程运行，系统登记的入口仍为 `start.py`，PID、直接写入日志的文件描述符和监控器持有的卡锁均保留。启动项只需登记这一个入口。

每 10 秒输出一条整批实验进度，单图内部进度条停用；每 5 个外循环保存当前样本状态及全部 RNG。总量为 42,000 次重建、2,060,800 个有效外循环；HDPS 的两个超分任务保留作者代码的 43 步提前停止，其余任务为 50 步。普通日志格式可识别本次进度条。若需要面板中的累计进度、当前 Step 和 ETA，监控器的高级日志格式使用 Flow，并登记上述状态文件为 `status_json` 来源。该格式只是监控协议，实验算法仍为 HDPS、FlowDPS、FLAIR。Flow 协议将初始化计为第 0 步，状态文件目标为 2,060,801；实际采样总步数保存在 `total_outer_steps`。

任务 ID 使用 `hdps_author_main_20261111`，与状态文件中的 `taskId` 相同。监控器表单由用户保存，本次脚本修改没有更改或启用应用中的自动启动设置。

重跑同一入口会验证已完成结果的 PNG 哈希并跳过，未完成样本从断点继续；恢复时核对配置、算法、输入和代码指纹。完成结果的 JSON 与 PNG 为持久记录，提交后移除该样本临时断点。温和停止时，先核实状态中的 PID 与该绝对入口匹配，再发送 SIGTERM，脚本在外循环边界保存退出。

CPU 环境检查（不查询或分配 GPU）：

```bash
ssh lab-campus '/data2/cy/xzn/envs/hdps_repro/bin/python /data2/cy/xzn/Code/HDPS/repro_outputs/hdps_author_main_20261111/start.py --check'
```

手动使用 tmux 时先自行确认一张空卡，显式指定该卡的 UUID，再运行 `launch_tmux.sh`。会话名为 `hdps_author_main`，脚本不会自行选卡。由训练监控器自动启动时直接使用 `start.py`，无需调用这个手动辅助脚本。

后续多卡可为各 worker 分配不同卡及 `--num-shards` / `--shard-rank`，沿用每个样本的独立检查点；各 worker 需要分别登记状态和日志来源。本次没有创建额外 worker。
