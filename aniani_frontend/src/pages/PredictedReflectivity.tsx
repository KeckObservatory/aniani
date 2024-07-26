import React, { useState, useEffect } from 'react';

interface PredictedReflecivityInterface {
    [key: string]: string | number;
    install_date: string;
    measured_date: string;
    mirror: string;
    measurement_type: string;
    mirror_type: string;
    segment_id: number;
}

const PredictedReflecivity: React.FC = () => {

    const [data, setData] = useState<PredictedReflecivityInterface[]>([]);

    useEffect(() => {
    fetch('http://localhost:5000/getPredictReflectivity')
        .then(response => response.json())
        .then(data => setData(data))
        .catch(error => console.error('Error fetching data', data));

    }, []);

    return (
        <div>
            <h2>predicted reflectivity page</h2>
            <p>Current predictied reflectivity:</p>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );

}

export default PredictedReflecivity;