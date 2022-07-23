<script>
    import Question from "./Question.svelte";
    if (!localStorage.getItem("questions")) {
        localStorage.setItem("questions", "30");
    }
    let questions = parseInt(localStorage.getItem("questions")),
        selected = 0,
        array = [];
    $: {
        if (questions) get_stars_info(questions);
        let i = 1;
        array = Array.from({ length: questions }, a => {
            return i++;
        });
        console.log(array);
    }
    function change_question(i) {
        selected = i;
        console.log(selected);
    }

    let stars_info = {};
    function get_stars_info(x) {
        fetch(`/api/question/?length=${x}`, {
            method: "GET",
        })
            .then(res => res.json())
            .then(res => {
                stars_info = res;
                console.log(res);
            })
            .catch(err => {
                console.log(err);
            });
    }

    if (!localStorage.getItem("updated_at"))
        localStorage.setItem("updated_at", Date.now());
    let updated_at = localStorage.getItem("updated_at");
    setInterval(() => {
        if (updated_at !== localStorage.getItem("updated_at")) {
            setTimeout(() => {
                get_stars_info(questions);
            }, 500);
            updated_at = localStorage.getItem("updated_at");
        }
    }, 500);
</script>

<h1 class="text-3xl font-bold text-center">ICode代码共享</h1>
<br />
<hr />
<br />
<div class="text-lg m-4">
    <p>
        使用说明：由于不知道国赛有几道题因此没有写死题目数量，首先设置题目数量。贡献时请填写姓名、星星数和源代码。复制代码时建议选择“复制混淆后代码”以防查重；但是由于测试不充分，可能对于一些情况，混淆后的代码出现问题，因此留有“复制源代码”按钮备用。<b
            >服务器未做安全防护和备份容灾，请勿随意乱点页面上的任意按钮，服务器宕机对谁都没好处！</b
        >
    </p>
    <br />
    <span>请输入题目数量：</span>
    <input
        bind:value={questions}
        type="number"
        class="border focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
        min="10"
        max="1000"
        on:blur={localStorage.setItem("questions", questions)}
    />
    <button
        class="bg-blue-500 hover:bg-blue-700 rounded-md py-1 px-2 text-base text-white"
        on:click={get_stars_info(questions)}
    >
        刷新题目星星信息
    </button>
</div>
<p class="text-lg m-4">
    <span>没有星星</span>
    <span class="bg-yellow-600">1颗星星</span>
    <span class="bg-yellow-300">2颗星星</span>
    <span class="bg-green-300">3颗星星</span>
</p>
<div class="flex flex-row flex-wrap m-4">
    {#each array as i}
        <button
            on:click={change_question(i)}
            class="shadow-md min-w-75 min-h-50 rounded-lg border-transparent font-bold text-lg flex-1"
            class:bg-green-300={stars_info[i] === 3}
            class:bg-yellow-300={stars_info[i] === 2}
            class:bg-yellow-600={stars_info[i] === 1}
        >
            {i}
        </button>
    {/each}
</div>

{#if selected}
    <div class="m-12">
        <Question question={selected} />
    </div>
{/if}

<div style="height: 100px" />

<footer style="width: 100%; text-align:center">
    <a href="http://beian.miit.gov.cn/" target="_blank">
        <span>鲁ICP备2020034769号</span>
    </a>
    |
    <a href="https://github.com/Danny-Yxzl/icode-v2"> GitHub </a>
</footer>

<style>
    button {
        margin: 5px;
    }
</style>
