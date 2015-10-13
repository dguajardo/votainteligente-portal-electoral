# coding=utf-8
from elections.tests import VotaInteligenteTestCase as TestCase
from elections.models import Election
from elections.bin import SecondRoundCreator
from candidator.models import TakenPosition


class SecondRoundCreationTestCase(TestCase):
    def setUp(self):
        self.tarapaca = Election.objects.get(id=1)
        self.adela = self.tarapaca.candidates.get(id=4)
        self.carlos = self.tarapaca.candidates.get(id=5)

    def test_create_a_second_round(self):
        sc = SecondRoundCreator(self.tarapaca)
        sc.pick_one(self.adela)
        sc.pick_one(self.carlos)
        self.assertEquals(sc.candidates[0], self.adela)
        self.assertEquals(sc.candidates[1], self.carlos)
        sc.set_name('second Round election')

        second_round = sc.get_second_round()

        self.assertIsInstance(second_round, Election)

        self.assertEquals(second_round.name, 'second Round election')
        self.assertEquals(second_round.candidates.count(), 2)
        self.assertIn(self.adela, second_round.candidates.all())
        self.assertIn(self.carlos, second_round.candidates.all())

    def test_copy_questions(self):
        sc = SecondRoundCreator(self.tarapaca)
        sc.pick_one(self.adela)
        sc.pick_one(self.carlos)
        second_round = sc.get_second_round()
        self.assertEquals(second_round.categories.count(), self.tarapaca.categories.count())
        for category in self.tarapaca.categories.all():
            _category = second_round.categories.get(name=category.name)
            self.assertEquals(_category.topics.count(), category.topics.count())
            for topic in category.topics.all():
                _topic = _category.topics.get(label=topic.label)
                self.assertTrue(TakenPosition.objects.filter(topic=_topic, person=self.adela))
                self.assertTrue(TakenPosition.objects.filter(topic=_topic, person=self.carlos))
                for position in topic.positions.all():
                    self.assertTrue(_topic.positions.filter(label=position.label))
