import unittest
from ipynb.fs.defs.snumpy import SNumPy, Validator


class TestSNumPy(unittest.TestCase):
    def test_create_array(self):
        self.assertEqual(SNumPy._create_array(2, 2, 1), [[1, 1], [1, 1]])
        self.assertEqual(SNumPy._create_array(3, None, 0), [0, 0, 0])

    def test_ones_and_zeros(self):
        self.assertEqual(SNumPy.ones(2, 2), [[1, 1], [1, 1]])
        self.assertEqual(SNumPy.zeros(3), [0, 0, 0])

    def test_reshape(self):
        self.assertEqual(SNumPy.reshape(
            [1, 2, 3, 4], (2, 2)), [[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            SNumPy.reshape([1, 2, 3], (2, 2))

    def test_shape(self):
        self.assertEqual(SNumPy.shape([1, 2, 3]), (3,))
        self.assertEqual(SNumPy.shape([[1, 2], [3, 4]]), (2, 2))

    def test_append(self):
        self.assertEqual(SNumPy.append([1, 2], [3, 4]), [1, 2, 3, 4])
        self.assertEqual(SNumPy.append(
            [[1], [2]], [[3], [4]], axis=1), [[1, 3], [2, 4]])

    def test_get(self):
        self.assertEqual(SNumPy.get([[1, 2], [3, 4]], (0, 1)), 2)
        with self.assertRaises(IndexError):
            SNumPy.get([[1, 2], [3, 4]], (0, 2))

    def test_add(self):
        self.assertEqual(SNumPy.add([1, 2], [3, 4]), [4, 6])
        self.assertEqual(SNumPy.add([[1, 2], [3, 4]], [
                         [5, 6], [7, 8]]), [[6, 8], [10, 12]])

    def test_subtract(self):
        self.assertEqual(SNumPy.subtract([4, 6], [1, 2]), [3, 4])
        self.assertEqual(SNumPy.subtract([[6, 8], [10, 12]], [
                         [1, 2], [3, 4]]), [[5, 6], [7, 8]])

    def test_dotproduct(self):
        self.assertEqual(SNumPy.dotproduct([1, 2], [3, 4]), 11)
        self.assertEqual(SNumPy.dotproduct([[1, 2], [3, 4]], [
                         [5, 6], [7, 8]]), [[19, 22], [43, 50]])

    def test_scalar_multiply(self):
        self.assertEqual(SNumPy.scalar_multiply([1, 2, 3], 3), [3, 6, 9])
        self.assertEqual(SNumPy.scalar_multiply(
            [[1, 2], [3, 4]], 2), [[2, 4], [6, 8]])

    def test_aug_matrix(self):
        self.assertEqual(SNumPy.aug_matrix(
            [[1, 2], [3, 4]], [5, 6]), [[1, 2, 5], [3, 4, 6]])
        with self.assertRaises(ValueError):
            SNumPy.aug_matrix([[1, 2], [3, 4]], [5])

    def test_gaussian_elimination(self):
        result = (SNumPy.gaussian_elimination([[2, 1], [5, 7]], [11, 13]))
        self.assertAlmostEqual(result[0], 7.1, places=1)
        self.assertAlmostEqual(result[1], -3.2, places=1)
        with self.assertRaises(ValueError):
            SNumPy.gaussian_elimination([[1, 2], [2, 4]], [5, 10])
        with self.assertRaises(ValueError):
            SNumPy.gaussian_elimination([[1, 2]], [5, 10])


class TestSNumPyValidation(unittest.TestCase):

    def test_invalid_vector_input(self):
        with self.assertRaises(TypeError):
            Validator.is_vector(123)  # Non-list input
        with self.assertRaises(ValueError):
            Validator.is_vector([1, 2, "a"])  # Non-numeric elements

    def test_invalid_matrix_input(self):
        with self.assertRaises(TypeError):
            Validator.is_matrix(123)  # Non-list input
        with self.assertRaises(ValueError):
            Validator.is_matrix([[1, 2], [3, "a"]])  # Non-numeric elements

    def test_invalid_vector_or_matrix(self):
        with self.assertRaises(TypeError):
            Validator.is_vector_or_matrix(123)  # Non-list input
        with self.assertRaises(ValueError):
            Validator.is_vector_or_matrix([[1, 2], [3]])  # Irregular shape

    def test_validate_shape_for_append(self):
        # Test valid cases
        self.assertIsNone(Validator.validate_shape_for_append(
            [[1, 2]], [[3, 4]], 0))  # Valid matrix append row-wise
        self.assertIsNone(Validator.validate_shape_for_append(
            [[1], [2]], [[3], [4]], 1))  # Valid matrix append column-wise

        # Test invalid cases
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_append(
                [[1, 2]], [[3]], 0)  # Different matrix column counts
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_append(
                [[1, 2]], [3, 4], 0)  # Vector to matrix

    def test_validate_shape_for_add_subtract(self):
        # Test valid cases
        self.assertIsNone(Validator.validate_shape_for_add_subtract(
            [1, 2], [3, 4]))  # Valid vector addition/subtraction
        self.assertIsNone(Validator.validate_shape_for_add_subtract(
            [[1, 2]], [[3, 4]]))  # Valid matrix addition/subtraction

        # Test invalid cases
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_add_subtract(
                [1, 2, 3], [4, 5])  # Different vector lengths
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_add_subtract(
                [[1, 2]], [[3, 4, 5]])  # Different matrix dimensions

    def test_validate_shape_for_dotproduct(self):
        # Test valid cases
        self.assertIsNone(Validator.validate_shape_for_dotproduct(
            [1, 2], [3, 4]))  # Valid vector dot product
        self.assertIsNone(Validator.validate_shape_for_dotproduct(
            [[1, 2]], [[3], [4]]))  # Valid matrix dot product

        # Test invalid cases
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_dotproduct(
                [1, 2, 3], [4, 5])  # Different vector lengths
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_dotproduct(
                [[1, 2, 3]], [[4, 5]])  # Incompatible matrix dimensions

    def test_validate_shape_for_gaussian_elemination(self):
        # Test valid cases
        self.assertIsNone(Validator.validate_shape_for_gaussian_elemination(
            [[1, 2], [3, 4]], [5, 6]))
        self.assertIsNone(Validator.validate_shape_for_gaussian_elemination(
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]], [4, 5, 6]))

        # Test invalid cases
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_gaussian_elemination(
                [[1, 2], [3, 4]], [5, 6, 7])  # Incompatible dimensions
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_gaussian_elemination(
                [[1, 2], [3, 4, 3]], [5, 6])  # Not a square matrix
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_gaussian_elemination(
                [[1, 2]], [5, 6, 7])  # Wrong matrix input
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_gaussian_elemination(
                [[1, 2], [3, 4]], [[1, 2], [3, 4]])  # Wrong vector input

    def test_index_validation(self):
        with self.assertRaises(IndexError):
            Validator.validate_index_for_get(
                [[1, 2], [3, 4]], (1, 3))  # Out of bounds
        with self.assertRaises(ValueError):
            Validator.validate_index_for_get(
                [[1, 2], [3, 4]], '1,2')  # Invalid index format

    def test_reshape_validation(self):
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_reshape(
                [[1, 2], [3, 4]], (2, 2))  # Not a vector
        with self.assertRaises(ValueError):
            Validator.validate_shape_for_reshape(
                [1, 2, 3, 4], (3, 2))  # Incompatible shape


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
