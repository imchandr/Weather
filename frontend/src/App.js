import "./App.css";
import axios from "axios";
import React, { useEffect, useState } from "react";

export default function App() {
  const [showList, setShowList] = useState(false);
  const [places, setPlaces] = useState({});
  const [placesAdded, setPlacesToAdd] = useState([]);
  const [weatherData, setWeatherdata] = useState([]);
  const [activePlace, setActivePlace] = useState('');

  useEffect(() => {
    fetchPlaces();
  }, []);

  const fetchPlaces = () => {
    axios.get("https://opnweather-api.herokuapp.com/api/").then((response) => {
      setPlaces(response.data);
    });
  };

  const fetchWeatherDetails = (place) => {
    setActivePlace(place)
    axios
      .get(`https://opnweather-api.herokuapp.com/weather/api/${place}`)
      .then((response) => {
        const weatherDetails = response.data;
        const result = [];
        for (const property in weatherDetails) {
          result.push(weatherDetails[property]);
        }
        setWeatherdata(result);
      });
  };

  return (
    <div className="App">
      <div className="box">
        <h2 className="heading">Weather Forecast</h2>
        <div style={{ display: "flex", overflowX: "auto" }}>
          {placesAdded.length > 0 &&
            placesAdded.map((item, index) => {
              return (
                <div
                  onClick={() => fetchWeatherDetails(item.name)}
                  className="place"
                >
                  {item.name}
                </div>
              );
            })}
          <div className="place">
            <div>
              <div onClick={() => setShowList(!showList)}> Add More + </div>
              {showList
                ? places.map((item) => {
                    return (
                      <div
                        className="place"
                        onClick={() => {
                          let data = placesAdded;
                          let exists =
                            data.filter((i) => i.id === item.id).length > 0;
                          if (!exists) {
                            setPlacesToAdd([...data, item]);
                          }
                        }}
                      >
                        {item.name}
                      </div>
                    );
                  })
                : null}
            </div>
          </div>
        </div>
        <div style={{ marginTop: "5%" }}>4 Day Forecast {activePlace} </div>
        <div style={{ width: "100%", display: "flex", overflowX: "auto" }}>
          {weatherData.map((item) => {
            return (
              <div className="data">
                <h4>{item.date}</h4>
                <h4>{item.day}</h4>
                <h4>{item.dt} °C</h4>
                <h4>{item.desc}</h4>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}