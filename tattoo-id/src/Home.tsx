import React, { useRef } from 'react';
import './style.css'
import tattooImage from '/tattoo.png'
import contactImage from '/contact.png'
import { useNavigate } from 'react-router-dom';

function Home() {
    const navigate = useNavigate();
    const contactRef = useRef(null);

    const handleTraceButtonClick = () => {
        // Redirect to the upload page
        navigate('/upload');
    };

    const handleContactButtonClick = () => {
        // Scroll to the contact block if contactRef is not null
        if (contactRef.current) {
            (contactRef.current as HTMLElement).scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    const handleGithubButtonClick = () => {
        // Redirect to your GitHub page
        window.location.href = 'https://github.com/aquib1011/TattooTrace';
    };

  return (
    <div className="home-container">
        <div className="content">
            <h1>Trace Tattoos in Your Photos/Videos</h1>
            <p className="intro">
                We aim to leverage advanced image recognition technology <br />
                to identify tattoos that may be affiliated to <br />
                a specific gang or criminal syndicate.
            </p>
            <div className="buttons">
                <button className="trace-button" onClick={handleTraceButtonClick}>Trace it!</button>
                <button className="contact-button" onClick={handleContactButtonClick}>Contact Us</button>
            </div>
        </div>
        <div className="images-container">
            <img src={tattooImage} alt="Tattoo" className="tattoo-image" />
        </div>
        <div className="contact-block" ref={contactRef}>
            <div className="contact-info">
                <img src={contactImage} alt="Contact" className="contact-image" />
                <div className="contact-details">
                    <p>Contact Us:</p>
                    <p>Members: Aquib Iqbal, Yi-Ting Han, Atluri Naga Sai Sri Vybhavi</p>
                    <p>Our Email: aquibiqbal@umass.edu, yhan@umass.edu</p>
                </div>
                <button className="github-button" onClick={handleGithubButtonClick}>Our Github</button>
            </div>
        </div>
        
    </div>
  )
}

export default Home
