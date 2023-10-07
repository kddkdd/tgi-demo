import pytest


@pytest.fixture(scope="module")
def flash_starcoder_gptq_handle(launcher):
    with launcher("Narsil/starcoder-gptq", num_shard=2, quantize="gptq") as handle:
        yield handle


@pytest.fixture(scope="module")
async def flash_starcoder_gptq(flash_starcoder_gptq_handle):
    await flash_starcoder_gptq_handle.health(300)
    return flash_starcoder_gptq_handle.client


@pytest.mark.asyncio
@pytest.mark.private
async def test_flash_starcoder_gptq(flash_starcoder_gptq, response_snapshot):
    response = await flash_starcoder_gptq.generate(
        "def geometric_mean(L: List[float]):",
        max_new_tokens=20,
        decoder_input_details=True,
    )
    assert response.details.generated_tokens == 20
    assert response == response_snapshot


@pytest.mark.asyncio
@pytest.mark.private
async def test_flash_starcoder_gptq_default_params(
    flash_starcoder_gptq, response_snapshot
):
    response = await flash_starcoder_gptq.generate(
        "def geometric_mean(L: List[float]):",
        max_new_tokens=20,
        temperature=0.2,
        top_p=0.95,
        decoder_input_details=True,
        seed=0,
    )
    assert response.details.generated_tokens == 20
    assert response == response_snapshot


@pytest.mark.asyncio
@pytest.mark.private
async def test_flash_starcoder_gptq_load(
    flash_starcoder_gptq, generate_load, response_snapshot
):
    responses = await generate_load(
        flash_starcoder_gptq,
        "def geometric_mean(L: List[float]):",
        max_new_tokens=10,
        n=4,
    )

    assert len(responses) == 4
    assert all([r.generated_text == responses[0].generated_text for r in responses])

    assert responses == response_snapshot
