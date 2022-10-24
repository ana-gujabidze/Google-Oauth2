import axios from "axios";
import React, { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';


function LoremIpsum() {
    const redirectUri = "api/lorem_ipsum/"
    const [data, setData] = useState("");
    useEffect(() => {
        async function fetchData() {
            try{
                const response = await axios.get(`${location.origin}/${redirectUri}`, { // eslint-disable-line no-restricted-globals
                    headers: {
                    'Authorization': `Bearer ${localStorage.getItem("accessToken")}` 
                    }
                })
                console.log(response)
                setData(response.data);
            } catch(error){
                console.log("Error: ", JSON.stringify(error, null, 4));
                throw error;
            }
        }
        fetchData();
}, []);


  return (
    <div className={"lorem-ipsum"}>
    <Container>
        <h1>{data.title}</h1>
        <p>{data.paragraph}</p>
    </Container>
    </div>
);
}


export default LoremIpsum;