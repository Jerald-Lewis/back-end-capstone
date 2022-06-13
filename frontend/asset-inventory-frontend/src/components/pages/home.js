import React from 'react';
import homepageImage from '../../../images/support-keyboard.png'

export default function () {
    return (
        <div className='homepage-content-wrapper'>
            <div className='homepage-image'
                style={{
                    backgroundImage: `url(${homepageImage})`,
                    height: 500
                }}
            >
                <div className='homepage-content'
                    style={{
                        color: '#4DB9B8',
                        fontWeight: 'bolder'
                    }}
                >
                    <p>
                        Welcome to AlticeUSA DeskSide Support Tools<br/><br/>
                        Manage your Inventory and Learn 
                    </p>
                </div> 
            </div>
        </div>
    )
}