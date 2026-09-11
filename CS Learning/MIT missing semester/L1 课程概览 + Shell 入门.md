# 主题一：Shell

## Shell 是什么？

要打开 Shell 的**提示符**（即输入命令的地方），首先需要一个**终端**——它是与 Shell 交互的图形界面。你的设备很可能已预装了终端，如果没有也可以安装一个：

- **Linux**：按下 Ctrl + Alt + T（适用于大多数发行版），或者在应用菜单中搜索「终端（Terminal）」。
- **Windows**：按下 Win + R ，输入 `cmd` 或 `powershell` ，然后按下 Enter 。也可以在开始菜单中搜索「终端（Terminal）」或「命令提示符（Command Prompt）」。

在 Linux 和 macOS 上，这通常会打开 Bourne Again Shell，简称 bash。它是最广泛使用的 Shell 之一，语法与许多其他 Shell 类似。在 Windows 上，可能会看到批处理（batch）或 PowerShell，具体取决于运行的命令，这些是 Windows 特有的。可以考虑使用 [适用于 Linux 的 Windows 子系统（WSL）](https://learn.microsoft.com/zh-cn/windows/wsl/) 或 Linux 虚拟机。

还有一些 Shell 在使用体验上对 bash 做了不少改进（例如 fish 和 zsh 是最常见的）。虽然它们很流行（授课教师们都在使用其中之一），但普及程度远不及 bash，而且依赖的许多概念也与 bash 相同。

## 在 Shell 中导航

当你打开终端时，会看到一个通常长这样子的**提示符**：

```
missing:~$
```

这是 Shell 的主要交互界面。它告诉你：你当前在名为 `missing` 的机器上，「当前工作目录」（即你所在的位置）是 `~`，它是 home 目录的简写，在 Linux 上通常对应 `/home/用户名`（例如 `/home/jon`）。  
`$` 表示你当前不是 root 用户。在提示符后输入命令，Shell 会解释并执行它。最基本的命令就是运行一个程序：

```
missing:~$ date
Fri 10 Jan 2020 11:49:31 AM EST
missing:~$
```

这里我们执行了 `date` 程序，它会（不出所料地）打印当前日期和时间。随后 Shell 会等待我们输入下一条命令。  
我们也可以带上**参数（_argument_）** 来执行命令：

```
missing:~$ echo hello
hello
```

在这个例子中，我们让 Shell 执行 `echo` 程序，并传入参数 `hello`。`echo` 的功能很简单：把收到的参数原样打印出来。Shell 解析这条命令时，会先按空白字符（空格、Tab 等）把整行拆分成若干部分，第一个单词就是要执行的程序，后面的每个单词都会作为参数传给它。  
如果参数本身包含空格或特殊字符（例如名为「My Photos」的目录），有两种处理方式：

- 用 `'` 或 `"` 把整个参数括起来，例如 `"My Photos"`
- 只对需要的字符进行转义，用反斜杠 `\`，例如 `My\ Photos`

对初学者来说最重要的命令大概是 `man`，即 manual（手册）的缩写。 `man` 可以帮你查询系统中任意命令的详细说明。比如运行 `man date`，它会告诉你 `date` 是什么、可以传入哪些参数来改变行为。对大多数命令来说，加上 `--help` 也能查看简短的帮助信息。

学会 `man` 之后，下一个最重要的是 `cd`（change directory，切换目录）。它实际上是 Shell 的内建命令，而不是独立程序（所以 `which cd` 会显示 `no cd found`）。给它传入一个路径，该路径就会成为你的当前工作目录，提示符也会随之变化。

```
missing:~$ cd /bin
missing:/bin$ cd /
missing:/$ cd ~
missing:~$
```

> [!note] NOTE
> 需要注意的是，Shell 通常自带自动补全功能，所以按下 Tab 往往能更快地补全路径
> 许多命令在未指定路径时，默认作用于当前工作目录。如果不确定自己在哪个目录，可以运行 `pwd`（print working directory，打印当前工作目录），或者查看 `$PWD` 环境变量（如 `echo $PWD`）。两者都会输出当前路径。

当前工作目录的另一重要作用是让我们能够使用**相对路径**。到目前为止我们看到的都是**绝对路径**：以 `/` 开头，给出了从文件系统根目录到目标位置的完整路径。 实际使用中，相对路径更常用。之所以叫「相对」，是因为它们是相对于当前工作目录来解析的。对于相对路径（即**任何不以 `/` 开头的路径**），Shell 会先在当前工作目录中查找路径的第一部分，然后逐级向下查找。例如：

```
missing:~$ cd /
missing:/$ cd bin
missing:/bin$
```

每个目录里还都有两个「特殊路径」：`.` 和 `..` 。 其中，`.` 表示「当前目录」，`..` 表示「父目录」。例如：

```
missing:~$ cd /
missing:/$ cd bin/../bin/../bin/././../bin/..
missing:/$
```

大多数情况下，绝对路径和相对路径可以互换使用；但使用相对路径时，一定要清楚自己当前在哪个目录！

## Shell 中有哪些可用的程序？

但 Shell 怎么知道去哪找 `date` 或 `echo` 这样的程序呢？当 Shell 需要执行命令时，它会查询 `$PATH` 环境变量。这个变量列出一组目录，Shell 会在这些目录中搜索与命令名匹配的程序：

```
missing:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
missing:~$ which echo
/bin/echo
missing:~$ /bin/echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

运行 `echo` 时，Shell 识别出需要执行名为 `echo` 的程序，然后在 `$PATH` 中以冒号（`:`）分隔的目录列表里逐个搜索同名文件。找到后就运行它（**前提是该文件是可执行的**，这点稍后详述）。  
可以用 `which` 查看某个命令实际对应哪个文件。也可以完全绕过 `$PATH`，**直接给出要执行文件的完整路径**。

这也说明了一个办法：列出 `$PATH` 中所有目录的内容，就能知道 Shell 中有哪些程序可用。我们可以把目录路径传给 `ls` 程序来实现（名称取自「list」，用于列出文件）：

```
missing:~$ ls /bin
```

在大多数计算机上，这会**列出非常多的程序**，但我们只关注其中最重要的几个。先从简单的开始：

- `cat hello.txt`：打印 `hello.txt` 的全部内容
- `sort hello.txt`：将 `hello.txt` 的各行按字典序排序后输出
- `uniq hello.txt`：去除 `hello.txt` 中连续重复的行
- `sort -u hello.txt`: 排序后去除重复的行
- `head -n1 hello.txt` 和 `tail -n3 hello.txt`：分别打印 `hello.txt` 的前1行和后3行(默认为10行)

还有 `grep pattern hello.txt`，它会在指定文本文件中查找所有匹配 `pattern` 的行。这个命令非常实用，值得多花些时间了解，它的功能比你想象的要丰富得多。

这里的 `pattern` 实际上是**正则表达式（regular expression）**，可以描述非常复杂的匹配模式

除了指定单个文件，你也可以指定一个目录作为搜索范围（或者直接不写，默认就是当前目录 `.` ），并加上 `-r` 参数让 `grep` 递归搜索目录里的所有文本文件，输出匹配的行。

还有一些实用工具，使用方式稍微复杂一些。先看 `sed`——一个可编程的文件编辑器。它有自己的「小语言」，可以自动化地修改文件。最常见的用法是：

```
missing:~$ sed -i 's/pattern/replacement/g' hello.txt
```

这条命令会把 `hello.txt` 中所有的 `pattern` 替换为 `replacement` 。具体来说：

- `-i` 参数表示直接修改文件（inline），而不是只在终端输出替换后的内容
- `s/` 是 `sed` 语法里表示「替换」的意思
- 两个 `/` 用来分隔「匹配模式」和「替换内容」
- 结尾的 `/g` 表示在每一行中**替换所有匹配项**，而不仅仅是第一个

> [!note]
> `sed` 是 stream editor（流编辑器） 的缩写，最早设计用来对输入流中的文本进行自动化处理，而不仅仅是单个文件。  
> `s/` 为什么表示替换：在 `sed` 的命令语法里，`s` 就是 substitute（替换） 的首字母，表示「把匹配到的内容替换成其他内容」。  
> `/g` 为什么表示替换所有匹配项：结尾的 `g` 是 global（全局） 的意思，表示在每一行中替换所有匹配项，如果没有 `g` ，`sed` 只会替换每行的第一个匹配项。

和 `grep` 一样，这里的 `pattern` 也是正则表达式，可以描述非常复杂的匹配模式。此外，正则表达式替换还允许 `replacement` 引用匹配模式中的部分内容，我们稍后会通过例子演示这一点。

接下来是 `find`，它可以递归地查找满足特定条件的文件。比如：

```
missing:~$ find ~/Downloads -type f -name "*.zip" -mtime +30
```

这会在下载（Downloads）目录中查找所有超过 30 天的 ZIP 文件。

```
missing:~$ find ~ -type f -size +100M -exec ls -lh {} \;
```

这会在 home 目录中查找所有大于 100M 的文件并列出它们。注意，**`-exec` 接受一条命令**，命令以 `;` 结尾（因此需要像转义空格那样对它转义）。`find` 会把每个匹配文件的路径替换到 `{}` 的位置。

```
missing:~$ find . -name "*.py" -exec grep -l "TODO" {} \;
```

这会在当前工作目录下查找所有包含 TODO （这个大写单词）的 `.py` 文件。

`find` 的语法可能有点吓人，但希望这些例子能让你感受到它的实用！

接下来介绍 `awk`，它和 `sed` 一样有自己的小语言。如果说 `sed` 专门用来编辑文件，那 `awk` 则专门用来解析文件。 `awk` 最常见的用途是处理有规则格式的数据文件（比如 CSV），从每条记录（每一行）中提取你需要的部分：

```
missing:~$ awk '{print $2}' hello.csv
```

这条命令会打印 `hello.csv` 中每一行的第二列（默认以空白字符分隔，空格或制表符都算）。如果你的文件是逗号分隔的（CSV 文件常见格式），可以加上 `-F,` 参数：

```
missing:~$ awk -F, '{print $2}' hello.csv
```

这样就会把每一行按逗号分成列，然后打印第二列。

除了提取列，`awk` 还能做很多事——过滤行、计算统计、求和等。具体可以通过习题动手试试。

将这些工具组合起来，我们可以完成一些很酷的操作，比如：

```
missing:~$ ssh myserver 'journalctl -u sshd -b-1 | grep "Disconnected from"' \
  | sed -E 's/.*Disconnected from .* user (.*) [^ ]+ port.*/\1/' \
  | sort | uniq -c \
  | sort -nk1,1 | tail -n10 \
  | awk '{print $2}' | paste -sd,
postgres,mysql,oracle,dell,ubuntu,inspur,test,admin,user,root
```

这条命令从远程服务器抓取 SSH 日志（`ssh` 会在下一讲详细介绍），搜索断开连接的消息，从中提取用户名，最后输出出现次数最多的前 10 个用户名（逗号分隔）。一切都在一条命令里完成！我们把逐步拆解这条命令留作习题。

## Shell 语言（bash）

前面的例子引入了一个新概念：管道（`|`）。它可以把一个程序的输出连接到另一个程序的输入。之所以可行，是因为多数命令行程序在未给出 `file` 参数时，会从「标准输入」（通常即键盘）读取数据。`|` 会把前面程序的「标准输出」（通常打印在终端上的内容）作为后面程序的标准输入。借助这种机制，我们就能**把多个 Shell 程序组合（compose）起来**，这也是 Shell 如此高效的重要原因之一。

事实上，大多数 Shell（如 bash）本身都实现了一套完整的编程语言，就像 Python 或 Ruby 一样。它有变量、条件判断、循环和函数。你在 Shell 中执行命令时，本质上就是在编写一小段由 Shell 解释执行的代码。今天不会系统讲完 bash，但有几部分你会经常用到：

先说重定向：`> file` 把程序的标准输出写入 `file` 而不是显示在终端，方便后续分析。`>> file` 追加到 `file` 而不是覆盖。`< file` 让程序从 `file` 读取输入而不是从键盘。

> [!note]
> 这里正好提一下 `tee` 程序。`tee` 会把标准输入原样输出到标准输出（和 `cat` 一样），但**同时也会把内容写入文件**。所以像 `verbose cmd | tee verbose.log | grep CRITICAL` 这样的命令，既能把完整的详细日志保存到文件里，又能让终端里只保留筛选后的关键信息，保持终端整洁。

接着是条件语句：`if command1; then command2; command3; fi` 会先执行 `command1`，成功则继续执行 `command2` 和 `command3`。也可以加 `else` 分支。最常作为 `command1` 的是 `test` 命令，通常简写为 `[`，可用于判断「文件是否存在」（`test -f file` / `[ -f file ]`）或「字符串是否相等」（`[ "$var" = "string" ]`）等条件。bash 还有 `[[ ]]`，是 test 的一种更安全的内置形式，在引号处理等方面的怪异行为更少。

bash 还有两种循环：`while` 和 `for`。  
`while command1; do command2; command3; done` 逻辑与前面的 `if` 类似，不同在于：只要 `command1` 不报错，就不断重复执行循环体。  
`for varname in a b c d; do command; done` 会执行 `command` 四次，每次把 `$varname` 依次设为 `a`、`b`、`c`、`d`。  
实际使用中，你往往不需要手动列出这些值，而是用「命令替换（command substitution）」，例如：

```
for i in $(seq 1 10); do
```

这会执行 `seq 1 10`（输出 1 到 10 的所有整数），然后用该命令的输出替换整个 `$()`，得到一个循环 10 次的 `for` 循环。 在较早的代码中，你可能会看到用反引号（``for i in `seq 1 10`; do``）做同样的事；但现在应优先使用 `$()`，因为它支持嵌套。

虽然你**可以直接在提示符里写很长的 Shell 脚本**，但通常更推荐把它们写进 `.sh` 文件。例如，下面这个脚本会在循环中不断运行某个程序直到它失败；它只打印失败那次的输出，同时在后台对 CPU 施加压力（这在复现偶尔失败的测试（flaky test）时非常有用）。

```
#!/bin/bash
set -euo pipefail

# Start CPU stress in background
stress --cpu 8 &
STRESS_PID=$!

# Setup log file
LOGFILE="test_runs_$(date +%s).log"
echo "Logging to $LOGFILE"

# Run tests until one fails
RUN=1
while cargo test my_test > "$LOGFILE" 2>&1; do
    echo "Run $RUN passed"
    ((RUN++))
done

# Cleanup and report
kill $STRESS_PID
echo "Test failed on run $RUN"
echo "Last 20 lines of output:"
tail -n 20 "$LOGFILE"
echo "Full log: $LOGFILE"
```

这段代码包含不少新内容，值得花些时间深入理解，因为对编写实用的 Shell 脚本很有帮助。比如：用后台任务（`&`）并发运行程序、更复杂的 [Shell 重定向](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)、以及 [算术扩展](https://www.gnu.org/software/bash/manual/html_node/Arithmetic-Expansion.html)。

值得特别看一下这个程序的前两行。  
第一行是「解释器指示行（shebang）」，你在很多脚本文件开头都会看到。 当以 `#!/path` 开头的文件被执行时，Shell 会启动 `/path` 指向的程序，把文件内容作为输入传给它。 对 Shell 脚本来说，就是把脚本内容交给 bash；但你也可以写 Python 脚本，用 `/usr/bin/python` 作为 shebang。 第二行让 bash 以更「严格」的模式运行，可以避免很多 Shell 脚本中常见的陷阱。`set` 接受很多参数，简单说：

- `-e` 表示任何命令失败时脚本立即退出
- `-u` 表示使用未定义变量时直接报错，而不是默默当作空字符串
- `-o pipefail` 表示在 `|` 管道序列中，只要有程序失败，整个脚本也会尽早退出

# 练习

1. 本课程要求你使用类 Unix 的 Shell，如 Bash 或 ZSH 。若你在 Linux 或 macOS 上，无需额外设置。若你在 Windows 上，请确认你用的不是 `cmd.exe` 或 `PowerShell`；你可以使用 [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) 或 Linux 虚拟机来获得 Unix 风格的命令行工具。要确认当前 Shell 是否合适，可运行 `echo $SHELL`；若输出类似 `/bin/bash` 或 `/usr/bin/zsh` ，就说明没问题。
    
2. `ls` 的 `-l` 选项（flag）作用是什么？运行 `ls -l /` 并观察输出。每一行最前面的 10 个字符分别代表什么？（提示：`man ls`）
	每行开头的 **10 个字符代表文件类型和权限**

| 位置<center></center> | 含义      | 示例        |
| ------------------- | ------- | --------- |
| 第1位                 | 文件类型    | ``-``普通文件 |
| 第2-4位               | 文件所有者权限 | ``rwx``   |
| 第5-7位               | 所属用户组权限 | ``r-x``   |
| 第8-10位              | 其他用户权限  | ``r--``   |
权限字符含义：
- `r`：read，可读
- `w`：write，可写
- `x`：execute，可执行
- `-`：没有该权限

3. 在命令 `find ~/Downloads -type f -name "*.zip" -mtime +30` 中，`*.zip` 是一个 「glob」。什么是 glob ？新建一个测试目录并创建一些文件，试试 `ls *.txt` 、`ls file?.txt` 、`ls {a,b,c}.txt` 等模式。参见 Bash 手册中的 [Pattern Matching](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html) 。
	**Glob** 是一种用于匹配文件名的简单模式，也叫“通配符模式”

| 模式      | 含义               | 示例                         |
| ------- | ---------------- | -------------------------- |
| `*`     | 任意数量的字符          | `*.txt` 匹配所有 `.txt` 文件     |
| `?`     | 任意一个字符           | `file?.txt` 匹配 `file1.txt` |
| `[abc]` | `a`、`b`、`c` 中的一个 | `file[123].txt`            |
| `[0-9]` | 指定范围内的一个字符       | `img[0-9].png`             |
4. `'单引号'`、`"双引号"` 和 `$'ANSI 引号'` 有什么区别？写一条命令，输出一个同时包含字面量 `$` 、`!` 和换行符的字符串。参见 [Quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html) 。 
	单引号 `'...'`内容几乎完全按字面解释：不会进行变量替换、命令替换，也不会解释 `\n`
	双引号 `"..."`会进行变量替换和命令替换但不会进行单词分割和通配符展开，因此适合保护包含空格的变量。
	ANSI-C 引号 `$'...'`支持转义字符：
	例如，下面的命令会输出字面量 `$`、`!` 和换行符：
	```bash
	printf '%s' $'字面量：$ ' '!' $'\n下一行\n'
	```

5. Shell 有三条标准流：stdin（0）、stdout（1）、stderr（2）。运行 `ls /nonexistent /tmp` ，把 stdout 和 stderr 分别重定向到两个文件。你将如何把两者都重定向到同一个文件？参见 [Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html) 。
```text
stdin   0：标准输入
stdout  1：标准输出
stderr  2：标准错误
```
先分别重定向
```bash
ls /nonexistent /tmp > stdout.txt 2> stderr.txt
```
把两者重定向到同一个文件
```bash
ls /nonexistent /tmp > all.txt 2>&1
```

6. `$?` 保存上一条命令的退出状态（0 表示成功）。`&&` 仅在前一条成功时执行后一条；`||` 仅在前一条失败时执行后一条。写一个一行命令：仅当 `/tmp/mydir` 不存在时才创建它。参见 [Exit Status](https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html) 。
	```bash
	[ -e /tmp/mydir ] || mkdir /tmp/mydir
	```
	`[ -e /tmp/mydir ]` 判断路径是否存在；如果判断失败，`||` 才会执行 `mkdir`。
	
7. 为什么 `cd` 必须是 Shell 内建命令，而不能是独立程序？（提示：想想子进程能影响和不能影响父进程的哪些状态。）
	普通外部命令通常在子进程中运行。即使子进程改变了自己的当前目录，也不会影响父进程，也就是当前的 Shell。`cd` 必须直接运行在当前 Shell 中，才能改变后续命令使用的工作目录。

8. 写一个脚本，接收文件名参数（`$1`），用 `test -f` 或 `[ -f ... ]` 检查该文件是否存在，并根据结果输出不同提示。参见 [Bash Conditional Expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html) 。
	```bash
	#!/usr/bin/env bash

	if [ "$#" -ne 1 ]; then
	    echo "用法：$0 文件名"
	    exit 2
	fi

	if [ -f "$1" ]; then
	    echo "文件存在：$1"
	else
	    echo "文件不存在，或它不是普通文件：$1"
	fi
	```

9. 把上一题完成的脚本保存为文件（如 `check.sh`）。先运行 `./check.sh somefile` ，会发生什么？然后执行 `chmod +x check.sh` 再试一次。为什么这一步是必须的？（提示：比较 `chmod` 前后的 `ls -l check.sh` 输出）
	未添加执行权限时运行：
	```bash
	./check.sh somefile
	```
	通常会得到 `Permission denied`。执行：
	```bash
	chmod +x check.sh
	ls -l check.sh
	```
	权限字符串中会增加 `x`，例如从 `-rw-r--r--` 变为类似 `-rwxr-xr-x`，此时才能直接执行 `./check.sh`。也可以不添加执行权限，直接运行 `bash check.sh somefile`。

10. 在脚本的 `set` 选项（flag）里加入 `-x` 会发生什么？写个简单脚本试试并观察输出。参见 [The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) 
	`set -x` 会在执行每条命令前，将展开后的命令打印出来，常用于调试：
	```bash
	#!/usr/bin/env bash
	set -x

	name="Tom"
	echo "Hello, $name"
	```
	输出中会出现类似：
	```text
	+ name=Tom
	+ echo 'Hello, Tom'
	Hello, Tom
	```
	关闭追踪可以使用 `set +x`。注意不要让密码等敏感信息被打印出来。

11. 写一条命令，把文件复制为带当天日期的备份文件名（例如 `notes.txt` → `notes_2026-01-12.txt`）。（提示：`$(date +%Y-%m-%d)`）参见 [Command Substitution](https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html) 。
	```bash
	cp notes.txt "notes_$(date +%Y-%m-%d).txt"
	```
	`$(date +%Y-%m-%d)` 会被替换为当天的日期。

12. 修改讲义中的「复现偶尔才会失败的测试」脚本（flaky test），使它能够从命令行参数接收测试命令，而不是在脚本中写死 `cargo test my_test`。（提示：`$1` 或 `$@`）参见 [Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html) 。
	把原脚本中的：
	```bash
	while cargo test my_test > "$LOGFILE" 2>&1; do
	```
	改为：
	```bash
	while "$@" > "$LOGFILE" 2>&1; do
	```
	然后可以这样运行：
	```bash
	./flaky.sh cargo test my_test
	```
	`"$@"` 会把脚本接收到的所有参数作为独立参数传给测试命令。

13. 使用管道找出你「home 目录」中最常见的 5 种文件扩展名。（提示：组合 `find` 、`grep` / `sed` / `awk`、`sort`、`uniq -c` 以及 `head`）
	```bash
	find "$HOME" -type f -printf '%f\n' 2>/dev/null |
	awk '
	  /\./ && $0 !~ /^\.[^.]+$/ {
	      name = $0
	      sub(/^.*\./, "", name)
	      print tolower(name)
	  }
	' |
	sort |
	uniq -c |
	sort -nr |
	head -n 5
	```
	这里取文件名最后一个点号后的部分作为扩展名，然后统计并按出现次数降序排列。

14. `xargs` 会把 stdin 的每一行转换为命令参数。结合 `find` 和 `xargs`（不要用 `find -exec`），找出目录中所有 `.sh` 文件，并用 `wc -l` 统计每个文件行数。加分项：正确处理文件名中的空格。（提示：`-print0` 和 `-0`）参见 `man xargs` 。
	```bash
	find . -type f -name "*.sh" -print0 |
	xargs -0 -r wc -l
	```
	`-print0` 和 `-0` 使用空字符分隔文件名，因此可以正确处理文件名中的空格。

15. 使用 `curl` 获取 [课程网站](https://missing.csail.mit.edu/) 的 HTML，并通过 `grep` 统计列出了多少讲。（提示：找出每讲课程名称在那份 HTML 中的共性；用 `curl -s` 关闭进度输出。）
	统计当前 2026 课程链接：
	```bash
	curl -s https://missing.csail.mit.edu/ |
	grep -oE 'href="/2026/[^"]+/"' |
	wc -l
	```
	其中 `curl -s` 静默获取网页，`grep -oE` 只输出匹配到的课程链接，`wc -l` 统计链接数量。如果要统计主页中列出的多个年份课程，可以将正则表达式中的 `2026` 改为相应年份。

16. [`jq`](https://jqlang.github.io/jq/) 是处理 JSON 的强大工具。用 curl 获取示例数据 https://microsoftedge.github.io/Demos/json-dummy-data/64KB.json，再用 jq 提取 version 大于 6 的人员姓名。（提示：先 `jq` . 看结构；再试 `jq '.[] | select(...) | .name'`）
	```bash
	curl -s https://microsoftedge.github.io/Demos/json-dummy-data/64KB.json |
	jq -r '.[] | select(.version > 6) | .name'
	```
	`.[]` 遍历数组，`select(.version > 6)` 筛选对象，`.name` 提取姓名，`-r` 以普通文本输出。

17. `awk` 可以按列值过滤行并改写输出。例如，`awk '$3 ~ /pattern/ {$4=""; print}'` 会只输出第三列匹配 `pattern` 的行，并省略第四列。请写一个 `awk` 命令：只输出第二列大于 100 的行，并交换第一列和第三列。可用这条命令测试：`printf 'a 50 x\nb 150 y\nc 200 z\n'`
	```bash
	printf 'a 50 x\nb 150 y\nc 200 z\n' |
	awk '$2 > 100 { print $3, $2, $1 }'
	```
	输出：
	```text
	y 150 b
	z 200 c
	```

18. 拆解讲义中的 [SSH 日志处理管道](https://missing-semester-cn.github.io/2026/course-shell/#shell-%E8%AF%AD%E8%A8%80bash)：每一步分别做了什么？然后仿照它构建一个管道，从 `~/.bash_history`（或 `~/.zsh_history`）中找出你最常使用的 Shell 命令。
	原管道各步骤的作用：
	1. `ssh myserver '...'`：连接远程服务器并执行引号中的命令。
	2. `journalctl -u sshd -b-1`：查看上一次启动周期中的 `sshd` 服务日志。
	3. `grep "Disconnected from"`：筛选 SSH 断开连接记录。
	4. `sed -E 's/.../\\1/'`：用正则表达式提取用户名。
	5. `sort | uniq -c`：先排序，再统计每个用户名出现的次数。
	6. `sort -nk1,1 | tail -n10`：按次数排序并取最后 10 个结果。
	7. `awk '{print $2}'`：只保留用户名。
	8. `paste -sd,`：把多行结果用逗号连接起来。
	统计 Bash 历史中最常用的命令：
	```bash
	sed -E 's/^[[:space:]]*[0-9]+[[:space:]]+//' ~/.bash_history |
	awk 'NF { print $1 }' |
	sort |
	uniq -c |
	sort -nr |
	head -n 10
	```
	如果使用 Zsh，可以先去掉 Zsh 历史文件的时间戳格式：
	```bash
	sed -E 's/^: [0-9]+:[0-9]+;//' ~/.zsh_history |
	awk 'NF { print $1 }' |
	sort | uniq -c | sort -nr | head -n 10
	```
