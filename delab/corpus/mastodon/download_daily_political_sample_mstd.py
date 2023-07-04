from random import choice
from delab.corpus.mastodon.download_conversations_mastodon import download_conversations_mstd
from datetime import date, datetime

hashtags = [
    'politics',
    'currentaffairs',
    'news',
    'government',
    'worldnews',
    'elections',
    'voting',
    'democracy',
    'activism',
    'politicaldebate',
    'politicalnews',
    'politicalanalysis',
    'politicalissues',
    'publicpolicy',
    'leadership',
    'policy',
    'politicalscience',
    'politicalreform',
    'politicalparty',
    'politicalcampaign',
    'politicalcommentary',
    'politicalopinion',
    'politicalengagement',
    'politicalawareness',
    'politicalstrategy',
    'politicaldiscussion',
    'currentevents',
    'hottopics',
    'worldpolitics',
    'socialjustice',
    'humanrights',
    'climatechange',
    'equality',
    'economicpolicy',
    'immigration',
    'foreignpolicy',
    'healthcare',
    'education',
    'technology',
    'environment',
    'sustainability',
    'corruption',
    'activist',
    'protest',
    'socialchange',
    'equalityforall',
    'politicalactivism',
    'politicaldialogue',
    'progressive',
    'conservative',
    'liberal',
    'republican',
    'democrat',
    'independent',
    'grassroots',
    'policereform',
    'guncontrol',
    'voterregistration',
    'civilrights',
    'womensrights',
    'lgbtqrights',
    'racialjustice',
    'disabilityrights',
    'incomeinequality',
    'taxreform',
    'foreignrelations',
    'nationalsecurity',
    'waronterror',
    'peacebuilding',
    'diplomacy',
    'globalgovernance',
    'freespeech',
    'fakenews',
    'factchecking',
    'media',
    'journalism',
    'campaignfinance',
    'politicalcartoon',
    'politicalmemes',
    'politicalsatire',
    'politicalhumor',
    'governmentaccountability',
    'transparency',
    'lobbying',
    'electionfraud',
    'foreigninterference',
    'votingrights',
    'politicalreality',
    'youthengagement',
    'civicparticipation',
    'electoralreform',
    'politicalasylum',
    'refugeecrisis',
    'bordersecurity',
    'climateaction',
    'cleanenergy',
    'sustainabledevelopment',
    'educationreform',
    'edtech',
    'healthcarereform',
    'mentalhealth',
    'pandemicresponse',
    'technologyethics',
    'dataprivacy',
    'surveillance',
    'cybersecurity',
    'environmentaljustice',
    'ecology',
    'sustainableliving',
    'corporategovernance',
    'ethics',
    'consumerprotection',
    'urbanplanning',
    'rurallife',
    'BLM',
    'balcklivesmatter',
    'pride',
    'LBTQIA+',
    'translivesmatter',
    'transphobia',
    'accountability',
    'queer',
    'LGBT',
    'BlackTransLivesMatter']


def download_daily_political_sample_mstd(topic_string):
    hashtag = choice(hashtags)
    today = date.today()
    download_conversations_mstd(query=hashtag, topic=topic_string, since=today)
