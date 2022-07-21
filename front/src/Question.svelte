<script>
    export let question;

    const DOMAINS = ["//icode.yxzl.top", "//icode.qdzx.icu"];

    let solves = [];

    function update(x) {
        fetch(`/api/question/${x}/`)
            .then(res => res.json())
            .then(res => {
                res.sort((a, b) => {
                    if (a.stars !== b.stars) return b.stars - a.stars;
                    return b.time - a.time;
                });
                solves = res;
                console.log(res);
            });
    }

    $: update(question);

    const copy = ["复制源代码", "复制混淆后代码"];
    function copy_text(text, index) {
        console.log(text);
        const input = document.createElement("textarea");
        input.value = text;
        document.body.appendChild(input);
        input.select();
        document.execCommand("copy");
        document.body.removeChild(input);
        text = copy[index];
        copy[index] = "已复制";
        setTimeout(() => {
            copy[index] = text;
        }, 1500);
    }

    const new_answer = {
        name: localStorage.getItem("name", ""),
        stars: 0,
        code: "",
    };
    function submit() {
        if (new_answer.stars < 1 || new_answer.stars > 3) {
            alert("请输入1-3的星星数");
            return;
        }
        localStorage.setItem("name", new_answer.name);
        for (let i = 0; i < DOMAINS.length; i++) {
            fetch(`${DOMAINS[i]}/api/question/${question}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(new_answer),
            })
                .then(res => res.json())
                .then(res => {
                    console.log(res);
                    update(question);
                });
        }
        localStorage.setItem("updated_at", Date.now());
    }

    let del_ts = "";
    function del() {
        if (!del_ts) {
            return;
        }
        for (let i = 0; i < DOMAINS.length; i++) {
            fetch(`${DOMAINS[i]}/api/question/${question}/del/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    ts: parseFloat(del_ts),
                }),
            })
                .then(res => res.json())
                .then(res => {
                    console.log(res);
                    update(question);
                });
        }
        localStorage.setItem("updated_at", Date.now());
    }
</script>

<div>
    <h2 class="text-xl font-bold">第 {question} 题的答案</h2>
    <hr class="my-4" />
    {#each solves as solve}
        <p class="my-2 text-lg">
            贡献者：{solve.name} &emsp; 星星数：{#each Array(solve.stars) as _}★{/each}
            &ensp;
            <button
                class="bg-green-300 hover:bg-green-500 rounded-md py-1 px-2 text-base"
                on:click={() => copy_text(solve.code, 0)}
            >
                {copy[0]}
            </button>
            <button
                class="bg-green-300 hover:bg-green-500 rounded-md py-1 px-2 text-base"
                on:click={() => copy_text(solve.code_hx, 1)}
            >
                {copy[1]}
            </button>
        </p>
        <code>
            <pre>{solve.code}</pre>
        </code>
        <hr class="my-4" />
    {/each}
    <form>
        <p class="my-2 text-lg">提交新答案</p>
        <input
            name="name"
            bind:value={new_answer.name}
            placeholder="请输入姓名"
            class="border focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent my-2"
        />
        <input
            name="stars"
            bind:value={new_answer.stars}
            type="number"
            max="3"
            placeholder="请输入星星数"
            class="border focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent my-2"
        />
        <textarea
            class="border focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent w-full"
            placeholder="请输入你的代码"
            name="code"
            bind:value={new_answer.code}
            rows="15"
        />
        <button
            class="bg-blue-500 hover:bg-blue-700 rounded-md py-1 px-2 text-base text-white"
            type="button"
            on:click={submit}
        >
            提交
        </button>
    </form>
    <hr class="my-4" />
    <input
        bind:value={del_ts}
        placeholder="请输入要删除的答案ID"
        class="border focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent my-2"
    />
    <button
        class="bg-blue-500 hover:bg-blue-700 rounded-md py-1 px-2 text-base text-white"
        type="button"
        on:click={del}
    >
        删除答案
    </button>
</div>

<style>
    pre {
        background: #fafafa;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
</style>
