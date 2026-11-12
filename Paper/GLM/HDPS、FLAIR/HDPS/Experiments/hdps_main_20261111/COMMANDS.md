# 运行命令

```bash
ssh lab-campus
tmux attach -t hdps_main_gpu2
```

启动新会话前执行 launch_tmux.sh，它核验 GPU2 UUID、占用和可用显存；已有死 pane 时由管理员明确重启当前 pane。恢复使用同一 worker.sh，自动验证断点指纹并跳过已完成样本。

```bash
bash /data2/cy/xzn/Code/HDPS/repro_outputs/hdps_main_20261111/worker.sh
```

温和停止：只向该次任务 status.json 中已核实命令行的 PID 发送 SIGTERM；在下一个外循环保存断点并退出。
