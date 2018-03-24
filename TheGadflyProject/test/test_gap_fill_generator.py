import unittest
from gadfly.gap_fill_generator import GapFillGenerator


class GapFillGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.SOURCE_TEXT = """In the constant scorekeeping of where tech’s
        power centers are, two trends stand out in Asia: the continued rise of
        China as a tech titan and the slow decline of Japan’s once-mighty
        tech industry.

        Those currents were evident in two recent developments.

        On Thursday, Paul Mozur and Jane Perlez reported that American
        officials had blocked a proposed purchase of a controlling stake in a
        unit of the Dutch electronics company Philips by Chinese investors
        because the United States was fearful the deal would be used to
        further China’s push into microchips.

        At the center of the concerns was a material called gallium nitride,
        which was being used by the Philips unit in light-emitting diodes, but
        which has applications for military and space and can be helpful in
        semiconductors. The report illustrated how American officials have
        come to view China’s large and growing tech industry with misgivings.

        At the same time, Jonathan Soble and Paul Mozur reported that Sharp,
        one of Japan’s large consumer electronics companies and the biggest
        LCD producer, was leaning toward a takeover offer from the Taiwanese
        contract manufacturer Foxconn. The news underlined the decline of
        Japan’s once-famed consumer electronics companies, which have been
        undercut in recent years by lower-cost competition from China and
        South Korea."""
        self.gfg = GapFillGenerator(self.SOURCE_TEXT)

    def test_output_to_list_should_return_list_not_set(self):
        self.assertIsInstance(self.gfg.output_questions(), list)

    def test_output_to_list_keys_should_include_required_fields(self):
        output_keys = set(self.gfg.output_questions()[0].keys())
        required_keys = set(["question", "answer", "answer_choices"])
        self.assertTrue(output_keys.issuperset(required_keys))

    def test_answer_choice_should_be_none(self):
        answer_choices = [s.answer_choices
                          for s in self.gfg.generate_questions()
                          if s.answer_choices is not None]
        self.assertFalse(answer_choices)

    def test_should_generate_zero_questions_with_no_named_ents(self):
        source_sentence =\
            "Those currents were evident in two recent developments."
        gfg = GapFillGenerator(source_sentence)
        self.assertFalse(gfg.output_questions())

    def test_should_generate_one_question_with_one_named_ents(self):
        source_sentence =\
            "Those currents were evident in two recent developments " + \
            "in Iran."
        gfg = GapFillGenerator(source_sentence)
        self.assertEqual(1, len(gfg.output_questions()))

    def test_should_generate_one_question_with_two_named_ents(self):
        source_sentence =\
            "Those NSA targets were evident in two recent developments " + \
            "in Iran."
        gfg = GapFillGenerator(source_sentence)
        self.assertEqual(1, len(gfg.output_questions()))

    if __name__ == '__main__':
            unittest.main()
