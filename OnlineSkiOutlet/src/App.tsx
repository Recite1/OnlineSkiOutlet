import React, {useEffect, useState} from 'react'
import {Header, BrandHeader} from './Headers';
import Item from './Item'

function App() {

  const [backendData, setBackendData] = useState({itemInfo: [{_id: "", Item:"",Img:"",OldPrice:"",NewPrice:"",Link:"" }]})
  const [evoBackendData, setEvoBackendData] = useState({itemInfo: [{_id: "", Item:"",Img:"",OldPrice:"",NewPrice:"",Link:"" }]})
  const [timeData, setTimeData] = useState({timeInfo: [{TimeUpdated:""}]})

  useEffect(()=>{
    fetch("http://localhost:4000/sportinglife").then(
      response => response.json()
    ).then(
      data => {
        setBackendData(data)
      }
    )
  }, []);

  useEffect(()=>{
    fetch("http://localhost:4000/evo").then(
      response => response.json()
    ).then(
      data => {
        setEvoBackendData(data)
      }
    )
  }, []);

  useEffect(()=>{
    fetch("http://localhost:4000/updatedTime").then(
      response => response.json()
    ).then(
      data => {
        setTimeData(data)
      }
    )
  }, []);
  console.log(timeData.timeInfo)
  return (
    <div>
      <Header/>
      <BrandHeader store = "SportingLife" />
      <div className = "item-collections-container">
      {backendData.itemInfo.length === 1 ? (
        <span>Loading...</span>
      ) : (
        backendData.itemInfo.map((x) => (
          <Item key = {x._id} itemData = {x}></Item>
        ))
      )}
      </div>
      <div>
        <BrandHeader store = "Evo"/>
        <div className = "item-collections-container">
        {evoBackendData.itemInfo.length === 1 ? (
          <span>Loading...</span>
        ) : (
          evoBackendData.itemInfo.map((x) => (
            <Item key = {x._id} itemData = {x}></Item>
          ))
        )}
        </div>
      </div>
      {timeData.timeInfo.map((x) => (
            <span className = "updatedTime"> last updated: {x.TimeUpdated}</span>
          ))}
    </div>
  )
}

export default App
