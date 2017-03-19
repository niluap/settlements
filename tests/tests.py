import unittest
from tries import get_weight_at_depth
from tries import weight_of_layers
from tries import primary_stresses
from tries import get_modulus_at_depth

test_soil_layers_database = [[3, 5, 9, 11], [20, 17, 19.5, 18], [36, 46, 42, 22], [40, 58, 80, 37]]
test_layers = [0, 1, 3, 5, 9, 11]


class TestFunctions(unittest.TestCase):

    def test_getting_depth_at_ground_level(self):
        weight = get_weight_at_depth(test_soil_layers_database, 0)
        self.assertEquals(weight, 20)

    def test_getting_depth_in_first_layer(self):
        weight = get_weight_at_depth(test_soil_layers_database, 2)
        self.assertEquals(weight, 20)

    def test_getting_depth_in_second_layer(self):
        weight = get_weight_at_depth(test_soil_layers_database, 4)
        self.assertEquals(weight, 17)

    def test_getting_depth_in_last_layer(self):
        weight = get_weight_at_depth(test_soil_layers_database, 10)
        self.assertEquals(weight, 18)

    def test_weights(self):
        weights = list(map(lambda x: get_weight_at_depth(test_soil_layers_database, x), test_layers))
        self.assertEquals(weights, [20, 20, 20, 17, 19.5, 18])

    def test_layers_weight(self):
        one_layer_weight = weight_of_layers(test_layers, [20, 20, 20, 17, 19.5, 18])
        self.assertEquals(one_layer_weight, [20, 40, 34, 78, 36])

    def test_primary_stresses(self):
        stresses_11 = primary_stresses(test_layers, [20, 40, 34, 78, 36])
        self.assertEquals(stresses_11, [0, 20, 60, 94, 172, 208])

    def test_modulus(self):
        modules = list(map(lambda x: get_modulus_at_depth(test_soil_layers_database, x), test_layers))
        self.assertEquals(modules, [36, 36, 36, 46, 42, 22])

if __name__ == '__main__':
    unittest.main()
