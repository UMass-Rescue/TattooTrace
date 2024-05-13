import React, { useEffect, useState } from 'react';
import axios from 'axios';

function ImageGallery() {
    const [images, setImages] = useState([]);

    useEffect(() => {
        // Fetch the list of images from the backend
        const fetchImages = async () => {
            try {
                const response = await axios.get('http://localhost:5000/images/list');
                setImages(response.data);
            } catch (error) {
                console.error('Error fetching images:', error);
            }
        };

        fetchImages();
    }, []);

    const handleImageClick = async (imageName) => {
        try {
            const response = await axios.post('http://localhost:5000/analyze', {
                imagePath: `images/${imageName}`
            });
            alert(`Label: ${response.data.label}, Confidence: ${response.data.confidence}`);
        } catch (error) {
            console.error('Error analyzing image:', error);
        }
    };

    return (
        <div className="gallery-container">
            {images.map((imageName, index) => (
                <img key={index} 
                     src={`http://localhost:5000/images/${imageName}`} 
                     alt={imageName} 
                     onClick={() => handleImageClick(imageName)} 
                     style={{cursor: 'pointer', maxWidth: '100px', margin: '10px'}} />
            ))}
        </div>
    );
}

export default ImageGallery;
