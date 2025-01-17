import pytest
from abnumber import Chain, ChainParseError, Position
from abnumber.germlines import HUMAN_IMGT_IG_V, HUMAN_IMGT_IG_J


def test_imgt_61A():
    """Related to ANARCI issue: https://github.com/oxpig/ANARCI/issues/14"""
    assert Position.from_string('61A', 'H', 'imgt') > Position.from_string('61', 'H', 'imgt')
    seq = 'EVQLVESGGGLVQPGGSLRLSCAASGIILDYYPIGWFRQAPGKEREGVAFITNSDDSTIYTNYADSVKGRFTISRDKNSLYLQMNSLRAEDTAVYYCSSKASFLIGKDDQGIDAGEYDYWGQGTMVTVSS'
    with pytest.raises(NotImplementedError):
        chain = Chain(seq, 'imgt')


def test_light_chain_IMGT_position_21():
    # Check bug from ANARCI 2021.02.04
    # When numbering full Kappa chains, position IMGT 21 contains a gap
    # When numbering V gene only, position IMGT 21 contains an amino acid as expected
    # Test against this by making sure that same numbering is assigned when numbering V gene and VJ genes concatenated
    # https://github.com/oxpig/ANARCI/issues/17
    for germline in HUMAN_IMGT_IG_V['K']['aligned_sequences']:
        v_seq = HUMAN_IMGT_IG_V['K']['aligned_sequences'][germline].replace('-', '')
        first_j_gene = list(HUMAN_IMGT_IG_J['K']['aligned_sequences'].keys())[0]
        j_seq = HUMAN_IMGT_IG_J['K']['aligned_sequences'][first_j_gene].replace('-', '')
        vj_seq = v_seq + j_seq
        try:
            v_chain = Chain(v_seq, 'imgt')
            vj_chain = Chain(vj_seq, 'imgt')
        except Exception as e:
            print(e)
            continue
        v_positions = [str(p) for p in v_chain.positions]
        vj_positions = [str(p) for p in vj_chain.positions]

        len_limit = len(v_seq) - 20
        assert ','.join(v_positions[:len_limit]) == ','.join(vj_positions[:len_limit])
