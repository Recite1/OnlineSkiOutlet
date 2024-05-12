
function Item({itemData}: any){
    return <a className = "item-container" href = {itemData.Link} target="_blank" >
        <img className = {"product-img"} src = {itemData.Img}/>
        <span className = {"product-oldprice"}>Regular Price: ${itemData.OldPrice}</span>
        <span className = {"product-price"}>Sale Price: ${itemData.NewPrice}</span>
        <span className= {"product-name"}>{itemData.Item}</span>
        <span className= {"product-sale"}>{((parseInt(itemData.OldPrice) - parseInt(itemData.NewPrice))/parseInt(itemData.OldPrice) * 100).toFixed()} % OFF</span>
    </a>
}

export default Item;