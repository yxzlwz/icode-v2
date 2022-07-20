<script>
    import Question from "./Question.svelte";
    if (!localStorage.getItem("questions")) {
        localStorage.setItem("questions", "30");
    }
    let questions = parseInt(localStorage.getItem("questions")),
        selected = 0,
        array = [];
    $: {
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
</script>

<h1 class="text-3xl font-bold text-center">ICode总决赛</h1>
<br />
<hr />
<br />
<div class="text-lg m-4">
    <span>请输入题目数量：</span>
    <input
        bind:value={questions}
        type="number"
        class="border focus:outline-none focus:ring-2 focus:ring-purple-600 focus:border-transparent"
        min="10"
        max="100"
        on:blur={localStorage.setItem("questions", questions)}
    />
</div>
<div class="flex flex-row flex-wrap m-4">
    {#each array as i}
        <button
            on:click={change_question(i)}
            class="shadow-md min-w-75 min-h-50 rounded-lg border-transparent font-bold text-lg flex-1"
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

<style>
    button {
        margin: 5px;
    }
</style>
