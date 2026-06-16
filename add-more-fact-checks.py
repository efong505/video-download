"""
Add more fact-check items to the fact-checks DynamoDB table
"""

import boto3
import uuid
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('fact-checks')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

fact_checks = [
    {
        'claim': 'The Bible supports abortion rights and bodily autonomy',
        'verdict': 'false',
        'category': 'Religion',
        'explanation': 'Scripture consistently affirms the sanctity of life from conception. Psalm 139:13-16 describes God forming us in the womb. Jeremiah 1:5 states God knew us before birth. Exodus 21:22-25 prescribes penalties for causing miscarriage, treating the unborn as persons. Luke 1:41-44 describes John the Baptist leaping in Elizabeth\'s womb, showing personhood before birth. The Bible never supports ending innocent life.',
        'source': 'Various progressive religious groups',
        'source_url': ''
    },
    {
        'claim': 'Jesus was a socialist who would support wealth redistribution',
        'verdict': 'false',
        'category': 'Economics',
        'explanation': 'Jesus taught voluntary charity, not government-forced redistribution. He said "render unto Caesar" (Matthew 22:21), separating spiritual and civil duties. The parable of the talents (Matthew 25:14-30) rewards investment and productivity. 2 Thessalonians 3:10 states "if anyone will not work, neither shall he eat." Jesus condemned greed but affirmed private property rights and personal responsibility. Biblical charity is voluntary, not coerced.',
        'source': 'Progressive Christian activists',
        'source_url': ''
    },
    {
        'claim': 'The January 6th Capitol protest was worse than 9/11 or Pearl Harbor',
        'verdict': 'false',
        'category': 'Government',
        'explanation': 'This comparison is absurd and offensive. 9/11 killed 2,977 Americans; Pearl Harbor killed 2,403. January 6th resulted in one protester death (Ashli Babbitt, shot by police) and several officer deaths days later from various causes. No firearms were confiscated from protesters. The Capitol was cleared within hours. Comparing a protest that got out of hand to coordinated attacks that killed thousands is historical revisionism designed to demonize political opponents.',
        'source': 'Democratic politicians and mainstream media',
        'source_url': ''
    },
    {
        'claim': 'Trump incited violence with his January 6th speech',
        'verdict': 'false',
        'category': 'Government',
        'explanation': 'Trump\'s speech explicitly stated "I know that everyone here will soon be marching over to the Capitol building to peacefully and patriotically make your voices heard." He never called for violence. The timeline shows the breach began before his speech ended. Trump later told protesters to "go home in peace." He was acquitted in impeachment trial. Meanwhile, Democrats spent 2020 encouraging BLM riots that caused $2 billion in damage and dozens of deaths.',
        'source': 'Democratic Party and mainstream media',
        'source_url': ''
    },
    {
        'claim': 'There are more than two genders and sex is a spectrum',
        'verdict': 'false',
        'category': 'Science',
        'explanation': 'Basic biology confirms two sexes: male (XY chromosomes) and female (XX chromosomes). Rare intersex conditions (0.018% of population) are disorders of sexual development, not additional sexes. Every cell in the human body is male or female. Gametes are either sperm or eggs. Gender ideology conflates psychological feelings with biological reality. This is not science but political activism masquerading as science.',
        'source': 'LGBTQ+ activists and progressive educators',
        'source_url': ''
    },
    {
        'claim': 'Puberty blockers for children are safe and reversible',
        'verdict': 'false',
        'category': 'Health',
        'explanation': 'Puberty blockers have serious long-term effects: reduced bone density, impaired brain development, sterility, and stunted growth. The Tavistock clinic in UK was shut down over safety concerns. Sweden, Finland, and UK have restricted pediatric gender treatments due to lack of evidence and harm. Nearly 100% of children on blockers proceed to cross-sex hormones, suggesting they lock in rather than pause development. This is experimental medicine on children.',
        'source': 'Gender clinics and LGBTQ+ advocacy groups',
        'source_url': ''
    },
    {
        'claim': 'The 2020 election was the most secure in American history',
        'verdict': 'false',
        'category': 'Government',
        'explanation': 'The 2020 election had unprecedented irregularities: mass mail-in ballots with relaxed verification, ballot harvesting, drop boxes without chain of custody, poll watchers blocked, counting stopped simultaneously in swing states, vote spikes at 3am, more votes than voters in some counties. Courts refused to hear evidence on procedural grounds. Zuckerberg spent $400M on election administration in Democrat areas. Calling this "most secure" defies common sense and evidence.',
        'source': 'CISA and mainstream media',
        'source_url': ''
    },
    {
        'claim': 'Voter ID laws are racist and suppress minority votes',
        'verdict': 'false',
        'category': 'Government',
        'explanation': 'This claim assumes minorities are incapable of obtaining ID, which is itself racist. ID is required for countless activities: banking, flying, buying alcohol, renting, getting a job. Most developed nations require voter ID. Studies show no suppression effect. Georgia\'s 2021 election law increased minority turnout. The real goal of opposing voter ID is enabling fraud, not protecting minorities. Secure elections benefit everyone.',
        'source': 'Democratic Party and civil rights organizations',
        'source_url': ''
    },
    {
        'claim': 'Christianity is responsible for most wars and violence in history',
        'verdict': 'false',
        'category': 'Religion',
        'explanation': 'Atheist regimes killed far more: Stalin (20M), Mao (65M), Hitler (12M). The Crusades were defensive responses to 400 years of Islamic conquest. The Inquisition killed thousands over centuries, while atheist regimes killed millions in decades. Most wars are fought over territory, resources, and power, not religion. Christianity\'s core message is love, forgiveness, and peace. Blaming Christianity for violence ignores history and atheism\'s bloody record.',
        'source': 'New Atheist authors and secular activists',
        'source_url': ''
    },
    {
        'claim': 'The Bible condones slavery and is therefore immoral',
        'verdict': 'misleading',
        'category': 'Religion',
        'explanation': 'Biblical "slavery" was primarily indentured servitude for debt, not race-based chattel slavery. Mosaic law protected servants: rest on Sabbath, freedom after 7 years, punishment for abuse. Philemon shows Paul advocating for a slave\'s freedom. Galatians 3:28 declares equality in Christ. Christianity ultimately ended slavery: Wilberforce and abolitionists were motivated by Christian faith. The Bible regulated existing practices while planting seeds for their abolition.',
        'source': 'Atheist critics and progressive theologians',
        'source_url': ''
    },
    {
        'claim': 'School choice and vouchers hurt public education',
        'verdict': 'false',
        'category': 'Education',
        'explanation': 'Competition improves all schools. Studies show public schools improve when facing school choice. Parents, not government, should control their children\'s education. Public schools receive funding per student, so money follows the child. Vouchers help poor families escape failing schools. Teachers unions oppose choice to protect their monopoly, not to help children. School choice increases parental satisfaction and student outcomes.',
        'source': 'Teachers unions and public education advocates',
        'source_url': ''
    },
    {
        'claim': 'Homeschooling produces poorly socialized children',
        'verdict': 'false',
        'category': 'Education',
        'explanation': 'Research shows homeschoolers score higher on socialization metrics than public school students. They participate in sports, co-ops, church, community activities. Public schools often expose children to bullying, drugs, violence, and peer pressure. Homeschoolers learn from diverse age groups, not just same-age peers. College admissions officers actively recruit homeschoolers for their maturity and self-direction. This claim reflects bias, not evidence.',
        'source': 'Public education establishment',
        'source_url': ''
    },
    {
        'claim': 'The gender pay gap proves systemic discrimination against women',
        'verdict': 'misleading',
        'category': 'Economics',
        'explanation': 'The 77 cents figure compares all men to all women, ignoring hours worked, experience, education, field, and choices. When controlling for these factors, the gap nearly disappears. Women choose lower-paying fields (teaching vs. engineering), work fewer hours, take time off for children. Childless women in their 20s earn more than men. The Equal Pay Act (1963) already bans discrimination. The "gap" reflects choices, not discrimination.',
        'source': 'Feminist organizations and Democratic politicians',
        'source_url': ''
    },
    {
        'claim': 'Illegal immigrants commit fewer crimes than citizens',
        'verdict': 'misleading',
        'category': 'Government',
        'explanation': 'This claim uses flawed methodology. Every illegal immigrant has committed a crime (illegal entry). Sanctuary cities don\'t report immigration status, skewing data. Studies exclude federal crimes and immigration violations. Border states show higher crime rates. Victims include Kate Steinle, Mollie Tibbetts, Laken Riley. Even if rates were equal, these are preventable crimes. Legal immigration is welcome; illegal immigration brings unvetted individuals and undermines rule of law.',
        'source': 'Immigration advocacy groups',
        'source_url': ''
    },
    {
        'claim': 'Diversity, Equity, and Inclusion (DEI) programs improve workplace performance',
        'verdict': 'false',
        'category': 'Economics',
        'explanation': 'Studies show DEI training often increases racial tension and resentment. It promotes discrimination against whites and Asians through quotas. Merit-based hiring produces better results than identity-based hiring. DEI is neo-Marxist ideology dividing people by race. Companies adopt it to avoid lawsuits, not because it works. True diversity is diversity of thought, not skin color. DEI programs are corporate CRT that harm productivity and morale.',
        'source': 'Corporate HR departments and DEI consultants',
        'source_url': ''
    },
    {
        'claim': 'Banning books in schools is censorship and book burning',
        'verdict': 'false',
        'category': 'Education',
        'explanation': 'Parents have the right to determine age-appropriate content for children. Removing sexually explicit or ideologically inappropriate books from school libraries is not censorship—books remain available elsewhere. Schools curate collections; not every book belongs in elementary schools. Many "banned" books contain graphic sexual content, pornography, or political indoctrination. Protecting children from inappropriate material is responsible parenting, not censorship. Adults can still access these books.',
        'source': 'American Library Association and progressive activists',
        'source_url': ''
    },
    {
        'claim': 'Christian business owners must provide services for same-sex weddings',
        'verdict': 'false',
        'category': 'Religion',
        'explanation': 'The First Amendment protects religious freedom and free speech. Forcing Christians to participate in ceremonies violating their beliefs is compelled speech. Jack Phillips (Masterpiece Cakeshop) won at Supreme Court. Barronelle Stutzman, a florist, was persecuted for her faith. Tolerance is a two-way street. Same-sex couples can find willing vendors; they target Christians to force compliance. Religious liberty is a fundamental right, not bigotry.',
        'source': 'LGBTQ+ advocacy groups and civil rights organizations',
        'source_url': ''
    },
    {
        'claim': 'The mainstream media is objective and unbiased',
        'verdict': 'false',
        'category': 'Media',
        'explanation': '90% of journalists vote Democrat. Coverage of Trump was 92% negative (Harvard study). Media suppressed Hunter Biden laptop story before 2020 election. They promoted Russia collusion hoax for 3 years. COVID lab leak was called conspiracy theory, now acknowledged as likely. Media acts as propaganda arm for Democrats. They ignore Biden scandals while manufacturing Trump controversies. Trust in media is at all-time lows because they abandoned objectivity for activism.',
        'source': 'Mainstream media outlets',
        'source_url': ''
    },
    {
        'claim': 'Fossil fuels are destroying the planet and must be eliminated',
        'verdict': 'misleading',
        'category': 'Science',
        'explanation': 'Fossil fuels lifted billions from poverty and enabled modern civilization. Climate models have consistently overpredicted warming. CO2 is plant food; Earth is greening. Renewable energy is unreliable and requires fossil fuel backup. Electric vehicles rely on coal power and child-mined cobalt. Climate has always changed. Proposed solutions (Green New Deal) would destroy economy while China and India increase emissions. Adaptation and innovation, not economic suicide, is the answer.',
        'source': 'Climate activists and progressive politicians',
        'source_url': ''
    },
    {
        'claim': 'Traditional marriage is outdated and oppressive to women',
        'verdict': 'false',
        'category': 'Family',
        'explanation': 'Marriage between one man and one woman is God\'s design (Genesis 2:24, Matthew 19:4-6). Children thrive best with married biological parents. Marriage provides stability, commitment, and complementary roles. Biblical marriage is mutual submission (Ephesians 5:21-33), not oppression. Divorce and single parenthood correlate with poverty, crime, and dysfunction. Redefining marriage has led to its decline. Traditional marriage benefits women, children, and society.',
        'source': 'Feminist activists and progressive culture',
        'source_url': ''
    }
]

print("Adding 20 more fact-check items...")

for fc in fact_checks:
    fact_id = str(uuid.uuid4())
    item = {
        'id': fact_id,
        'claim': fc['claim'],
        'verdict': fc['verdict'],
        'category': fc['category'],
        'explanation': fc['explanation'],
        'source': fc['source'],
        'source_url': fc['source_url'],
        'submitted_by': PLATFORM_OWNER_ID,
        'created_at': datetime.now().isoformat(),
        'agree_votes': 0,
        'disagree_votes': 0,
        'voted_by': {}
    }
    
    table.put_item(Item=item)
    print(f"✅ Added: {fc['claim'][:60]}...")

print(f"\n✅ Successfully added {len(fact_checks)} fact-check items!")
print("\nCategories breakdown:")
categories = {}
for fc in fact_checks:
    cat = fc['category']
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")
