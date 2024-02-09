from src.commands.list_offer import ListOffer

class TestListOffer():

    def test_is_valid_token(self):
        listOffer = ListOffer()
        assert listOffer.is_valid_token("Bearer cd3d1303-2d62-4f60-8472-3349d34f690c") == True
