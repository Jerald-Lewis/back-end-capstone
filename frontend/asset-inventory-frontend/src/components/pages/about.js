import React from 'react';
import aboutImage from '../../../images/altice-group-pic.jpg'
import { Link } from 'react-router-dom';

export default function() {
    return (
    <div className='about-wrapper'>
        <div className='about-content'
              style={{
                background:"no-repeat",
                backgroundImage:`url(${aboutImage})`,
                height: 500,
              }}
              >
            <p>
                We are a group of analyst striving to provide top tier service to end-users.<br/><br/>
                Here you will have the ability to management your inventory and have one easy to navigate location to find knowledge that can assist with resolving end user issues. <br/><br/>
                We appreciate the input of all anaylst so provide feedback here.  This will help us improve.
            </p>
        </div>
    </div>
    );
}