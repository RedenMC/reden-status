import {useEffect, useState} from 'react'
import './App.css'
import {LineChart} from "@mui/x-charts";
import {Box} from "@mui/material";
import {DatePicker, LocalizationProvider} from "@mui/x-date-pickers";
import {AdapterDateFns} from "@mui/x-date-pickers/AdapterDateFnsV3";

function App() {
  type Status = {
    name: string;
    timestamp: number;
    status: number;
    value: number;
    online_count: number;
  }
  const [statusData, setStatusData] = useState<Status[]>([])
  const [filteredData, setFilteredData] = useState<Status[]>([])
  useEffect(() => {
    fetch("https://raw.githubusercontent.com/RedenMC/reden-status/main/data/status.json")
        .then(response => response.json())
        .then((data: {
          [key: string]: {
            timestamp: number;
            status: number;
            online_count: number;
          }
        }) => Object.entries(data).map(([name, status]) => {
          const obj: Status = {
            name,
            ...status,
            value: (status.status === 200 ? status.online_count : 0)
          }
          return obj
        })).then(statusData => {
      setStatusData(statusData);
      setFilteredData(statusData);
    });
  }, []);

  const [fromDate, setFromDate] = useState<Date | null>(null);
  const [toDate, setToDate] = useState<Date | null>(null);

  function filterByDate() {
    if (fromDate && toDate) {
      const filteredData = statusData.filter((status) => {
        return status.timestamp >= fromDate.getTime() && status.timestamp <= toDate.getTime();
      });
      setFilteredData(filteredData);
    }
  }

  return <>
    <Box sx={{flexGrow: 1, width: "90vw"}}>
      <LineChart
          height={300}
          axisHighlight={{x: "line"}}
          xAxis={
            [
              {
                data: filteredData.map((status) => status.timestamp),
                valueFormatter: (value) => {
                  return new Date(value).toLocaleString()
                }
              }
            ]
          }
          series={[
            {
              curve: "linear",
              showMark: false,
              area: true,
              data: filteredData.map((status) => status.value),
              valueFormatter: (value, {dataIndex}) => {
                const data = filteredData[dataIndex];
                if (data.status === 200)
                  return `${value} online`;
                else {
                  return `Server offline`;
                }
              }
            }
          ]} />
    </Box>
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      Filter by date:
      <Box>
        <DatePicker label={"From"} value={fromDate} onAccept={(date) => setFromDate(date)} />
        <DatePicker label={"To"} value={toDate} onAccept={(date) => setToDate(date)} />
      </Box>
      <Box>
        <button onClick={filterByDate}>OK</button>
      </Box>
      Copyright (c) <a href="https://redenmc.com/">RedenMC</a> All rights reserved.
    </LocalizationProvider>
  </>
}

export default App
