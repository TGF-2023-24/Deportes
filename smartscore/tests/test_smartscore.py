import pytest

from ..models import Player, Position
from ..smartscore import smartScore


@pytest.fixture
def messi():
    return Player.objects.create(
        Name="Lionel Messi",
        Club="Paris Saint-Germain",
        #League="Ligue 1",
        Nationality="Argentina",
        Pref_foot="Left",
        Age=34,
        Height=170,
        Weight=72,
        custom_id=1,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        International_match=20,
        Res_match=10,
        Min=1400,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=2.0,
        Poss_lost_90=9.5,
        Shot_rat=85,
        Conv_rat=20,
        Dorsal=7,
        Country_league="Test Country",
        market_value="15"
    )


@pytest.fixture
def player2():
    return  Player.objects.create(
        custom_id=2,
        Name="Test Player2",
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=0,
        League="Test League",
        Pref_foot="Left",
        Age=100,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=0,
        Pot_abil=0,
        Strater_match=0,
        Res_match=0,
        Min=600,
        Goal=0,
        Asis=0,
        xG=0,
        Gol_90=0,
        Asis_90=0.15,
        Goal_allowed=0,
        Clean_sheet=0,
        Sv_rat=0,
        xSv_rat=0,
        Pen_saved_rat=0,
        Faga=0,
        Fcomm=0,
        Yel=0,
        Red=0,
        Dist_90=0,
        Key_tck_90=0,
        Key_hdr_90=0,
        Blocks_90=0,
        Clr_90=0,
        Int_90=1.0,
        Hdr_rat=0,
        Tackles_rat=0,
        Gl_mistake=0,
        Pass_rat=0,
        Pr_pass_90=0,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value="8"
    )



@pytest.fixture
def player3():
    return  Player.objects.create(
        custom_id=3,
        Name="Test Player3",
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=70,
        League="Test League",
        Pref_foot="Left",
        Age=25,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        Res_match=10,
        Min=800,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value='Unknown',
    )

@pytest.fixture
def player4():
    return  Player.objects.create(
        custom_id=4,
        Name="Test Player4",
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=200,
        League="Test League2",
        Pref_foot="Left",
        Age=27,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=90,
        Strater_match=20,
        Res_match=10,
        Min=400,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value=160,
    )
    
@pytest.fixture
def player5():
    return  Player.objects.create(
        custom_id=5,
        Name="Test Player4",
        Club="Test Club",
        Nationality="Test Nationality",
        International_match=200,
        League="Test League2",
        Pref_foot="Left",
        Age=18,
        Height=180,
        Weight=75,
        Salary=50000,
        CAbil=80,
        Pot_abil=300,
        Strater_match=20,
        Res_match=10,
        Min=400,
        Goal=5,
        Asis=3,
        xG=4.5,
        Gol_90=0.25,
        Asis_90=0.15,
        Goal_allowed=10,
        Clean_sheet=3,
        Sv_rat=80,
        xSv_rat=75,
        Pen_saved_rat=70,
        Faga=20,
        Fcomm=15,
        Yel=2,
        Red=0,
        Dist_90=9.5,
        Key_tck_90=1.2,
        Key_hdr_90=0.8,
        Blocks_90=2.5,
        Clr_90=3.0,
        Int_90=1.8,
        Hdr_rat=85,
        Tackles_rat=75,
        Gl_mistake=1,
        Pass_rat=90,
        Pr_pass_90=85,
        Key_pass_90=2.0,
        Cr_c_90=3.5,
        Cr_c_acc=80,
        Ch_c_90=2.2,
        Drb_90=1.5,
        Poss_lost_90=8.5,
        Shot_rat=80,
        Conv_rat=15,
        Dorsal=10,
        Country_league="Test Country",
        market_value=150,
    )

@pytest.mark.django_db
def test_smartscore(messi, player2, player3, player4, player5):
    player = Player.objects.get(custom_id=1)

    Position.objects.create(id=1, name="STC")

    score = smartScore(player, "STC", 150, 2, "League 1")

    expected_score = 36
    assert score == expected_score

    player = Player.objects.get(custom_id=2)
    score = smartScore(player, "STC", 150, 1, "League 1")
    expected_score = 1
    assert score == expected_score

    player = Player.objects.get(custom_id=3)
    score = smartScore(player, "STC", 150, 0, "League 1")
    expected_score = 55
    assert score == expected_score

    player = Player.objects.get(custom_id=4)
    score = smartScore(player, "STC", 150, 2, "Unknown")
    expected_score = 29
    assert score == expected_score

    player = Player.objects.get(custom_id=5)
    score = smartScore(player, "STC", 150, 2, "Unknown")
    expected_score = 99
    assert score == expected_score
