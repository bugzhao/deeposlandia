"""Define a class that represents typical convolutional neural networks
"""

import keras as K

class ConvolutionalNeuralNetwork:
    """Convolutional neural network design

    Attributes
    ----------
    network_name : str
        Name of the network
    image_size : integer
        Input image size (height and width are equal)
    nb_channels : integer
        Number of input image channels (1 for greyscaled images, 3 for RGB images)
    nb_labels : integer
        Number of classes in the dataset glossary
    X : tensor
        (batch_size, image_size, image_size, nb_channels)-shaped input tensor; input image data

    """

    def __init__(self, network_name="mapillary", image_size=512,
                 nb_channels=3, nb_labels=65, learning_rate=1e-4):
        self.network_name = network_name
        self.image_size = image_size
        self.nb_channels = nb_channels
        self.nb_labels = nb_labels
        self.X = K.layers.Input(shape=(image_size, image_size, nb_channels), name="input")

    def layer_name(self, prefix, suffix):
        """Concatenate prefix and suffix to build a complete layer name

        Use the default Keras behavior if prefix is None

        Parameters
        ----------
        prefix : str
            Layer name prefix, refers to the layer block
        suffix : str
            Layer name suffix, refers to the layer type

        Returns
        -------
        str
            Complete layer name, build as prefix + suffix
        """
        return prefix + suffix if prefix is not None else None

    def convolution(self, x, nb_filters, kernel_size, strides=1, padding="same",
                    activation='relu', batch_norm=True, block_name=None):
        """Apply a convolutional layer within a neural network

        Use Keras API

        Parameters
        ----------
        x : tensor
            Input layer
        nb_filters : integer
            Number of convolution filters
        kernel_size : integer
            Convolution filter size, in pixel
        strides : integer
            Convolution strides, in pixel
        padding : str
            Border pixel management ("valid" to apply convolution pixel only on image pixels, or
        "same" to replicate border pixels)
        activation : str
            Type of activation function to apply on the tensor at the end of the convolution block
        ('relu' by default)
        batch_norm : boolean
            If True, a batch normalization process is applied on `x` tensor before activation
            layer
        block_name : str
            Convolution block name, for identification purpose

        Returns
        -------
        tensor
            4D output layer
        """
        x = K.layers.Conv2D(nb_filters, kernel_size=kernel_size, strides=strides,
                            padding='same', name=self.layer_name(block_name, '_conv'))(x)
        if batch_norm:
            x = K.layers.BatchNormalization(name=self.layer_name(block_name, '_bn'))(x)
        x = K.layers.Activation(activation, name=self.layer_name(block_name, '_activation'))(x)
        return x

    def transposed_convolution(self, x, nb_filters, kernel_size, strides=1,
                               padding="same", activation='relu', batch_norm=True, block_name=None):
        """Build a layer seen as the transpose operation of classic convolution, for a convolutional neural
        network

        Use Keras API

        Parameters
        ----------
        x : tensor
            Input tensor
        nb_filters : integer
            Number of convolution filters
        kernel_size : integer
            Convolution filter size, in pixel
        strides : integer
            Convolution strides, in pixel
        padding : str
            Border pixel management ("valid" to apply convolution pixel only on image pixels, or
        "same" to replicate border pixels)
        activation : str
            Type of activation function to apply on the tensor at the end of the convolution block
        ('relu' by default)
        batch_norm : boolean
            If True, a batch normalization process is applied on `x` tensor before activation
            layer
        block_name : str
            Transposed convolution block name, for identification purpose

        Returns
        -------
        tensor
            4D output layer
        """
        x = K.layers.Conv2DTranspose(nb_filters, kernel_size=kernel_size, strides=strides,
                                     padding=padding, name=self.layer_name(block_name, '_transconv'))(x)
        if batch_norm:
            x = K.layers.BatchNormalization(name=self.layer_name(block_name, '_bn'))(x)
        x = K.layers.Activation(activation, name=self.layer_name(block_name, '_activation'))(x)
        return x

    def maxpool(self, x, pool_size, strides=1, padding="same", block_name=None):
        """Apply a max pooling layer within a neural network

        Use Keras API

        Parameters
        ----------
        x : tensor
            Input layer
        pool_size : integer
            Pooling kernel size, in pixel
        strides : integer
            Pooling strides, in pixel ; indicates the downscaling factor
        padding : str
            Border pixel management ("valid" to apply convolution pixel only on image pixels, or
        "same" to replicate border pixels)
        block_name : str
            Pooling block name, for identification purpose

        Returns
        -------
        tensor
            4D output layer
        """
        return K.layers.MaxPool2D(pool_size=pool_size, strides=strides, padding=padding, name=block_name)(x)

    def dense(self, x, depth, dropout_rate=1.0, activation='relu', batch_norm=True, block_name=None):
        """Apply a fully-connected layer within a neural network

        Use Keras API

        Parameters
        ----------
        x : tensor
            Input layer
        depth : integer
            Number of neurons used within the layer
        activation : str
            Type of activation function to apply on the tensor at the end of the convolution block
        ('relu' by default)
        dropout_rate: tensor
            tensor corresponding to the neuron keeping probability during dropout operation
        batch_norm : boolean
            If True, a batch normalization process is applied on `x` tensor before activation
            layer
        block_name : str
            Fully-connected block name, for identification purpose

        Returns
        -------
        tensor
            Output layer
        """
        x = K.layers.Dense(depth, name=self.layer_name(block_name, '_fc'))(x)
        if batch_norm:
            x = K.layers.BatchNormalization(name=self.layer_name(block_name, '_bn'))(x)
        x = K.layers.Activation(activation, name=self.layer_name(block_name, '_activation'))(x)
        x = K.layers.Dropout(dropout_rate, name=self.layer_name(block_name, '_dropout'))(x)
        return x

    def flatten(self, x, block_name=None):
        """Apply a flattening operation to input tensor `x`, to reduce its dimension; arises
        generally before a dense layer

        Parameters
        ----------
        x : tensor
            Input layer; its shapes is necessarily larger than 3
        block_name : str
            Flatten block name, for identification purpose

        Returns
        -------
        tensor
            2D output layer
        """
        return K.layers.Flatten(name=block_name)(x)
