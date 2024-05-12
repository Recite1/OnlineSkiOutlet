import { Fragment ,useState } from "react";
interface props {
    store: string;
}
export function Header(){

    function fix(name : string){
        const element = document.getElementById(name) as HTMLElement;
        console.log(element.offsetTop)
        const targetPosition = element.offsetTop - 100;

        window.scrollTo({
            top: targetPosition,
            behavior: 'smooth' // Smooth scrolling
        }); 
    }

    return <div className = "header">
        <a className = "slStoreButton" onClick = {() => fix("SportingLife-header")}>SportingLife</a>
        <span className = "logo"> Online Ski Outlet</span>
        <a className = "evoStoreButton"  onClick = {() => fix("Evo-header")}>EVO</a>

    </div>;
}

export function BrandHeader({store}: props){
    return <div id = {store + "-header"}>
        <img src= {"/" + store  + "Logo.png" } alt= {store}/>
    </div>;
}
