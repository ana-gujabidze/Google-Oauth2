import React, { useEffect, useState } from "react";
import Container from 'react-bootstrap/Container';
import axiosInstance from "../axiosApi.js";

function LoremIpsum() {
    const redirectUri = "lorem_ipsum/"
    const [data, setData] = useState("");
    useEffect(() => {
        async function fetchData() {
            try {
                const response = await axiosInstance.get(redirectUri)
                setData(response.data);
            } catch (error) {
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