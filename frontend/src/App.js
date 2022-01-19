import { useState } from 'react';
import axios from 'axios';
import DateTimePicker from 'react-datetime-picker';
import './App.css';

function App() {
  // states to keep track of the pirce and form data
  const [price, setPrice] = useState(0);
  const [formData, setFormData] = useState({
    cart_value: 1,
    delivery_distance: 1,
    number_of_items: 1,
    time: new Date()
  });

  // For changes in the form
  const onChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });
  const onSubmit = (e) => {
    e.preventDefault();

    const config = {
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const time = formData.time;
    // Construct timeString with the desiered format
    const timeString = `${time.getUTCFullYear()}-${time.getUTCMonth() + 1}-${time.getUTCDate()}T${time.getUTCHours()}:${time.getUTCMinutes()}:${time.getUTCSeconds()}Z`;
    const body = {
      'cart_value': formData.cart_value,
      'delivery_distance': formData.delivery_distance,
      'number_of_items': formData.number_of_items,
      'time': timeString
    }

    // make request
    // TODO put link 'http://localhost:8000' in a .env file
    axios.post('http://localhost:8000/calculator/', body, config)
      .then((res) => {
        setPrice(res.data['delivery_fee']);
      })
      .catch((err) => {
        // TODO handle error better, not that there is much chance of an error here for the time being
        console.log(err);
      });
  }

  return (
    <div className="">
      <div className="container">
        {/* A from copied from bootstrap */}
        <form onSubmit={onSubmit}>

          <legend className="mb-3">Delivery Fee Calculator</legend>

          {/* Cart value field */}
          <div className="mb-3 row">

            <label htmlFor="cartValue" className="col-sm-2 col-form-label">Cart Value</label>

            <div className="col-sm-9">
              <input type="number" className="form-control" id="cartValue" name="cart_value" value={formData.cart_value} onChange={onChange} min="1" />
            </div>

            <div className="col-sm-1 col-form-label">€</div>
          </div>

          {/* Delivery distance field */}
          <div className="mb-3 row">

            <label htmlFor="deliveryDistance" className="col-sm-2 col-form-label">Delivery distance</label>

            <div className="col-sm-9">
              <input type="number" className="form-control" id="deliveryDistance" name="delivery_distance" value={formData.delivery_distance} onChange={onChange} min="1" />
            </div>

            <div className="col-sm-1 col-form-label">m</div>
          </div>

          {/* Item count field */}
          <div className="mb-3 row">

            <label htmlFor="ammountOfItems" className="col-sm-2 col-form-label">Ammount of Items</label>

            <div className="col-sm-9">
              <input type="number" className="form-control" id="ammountOfItems" name="number_of_items" value={formData.number_of_items} onChange={onChange} min="1" />
            </div>
          </div>

          {/* Time of delivery field */}
          <div className="mb-3 row">

            <label htmlFor="time" className="col-sm-2 col-form-label">Time</label>

            <div className="col-sm-9">
              {/* A downloadable date time picker */}
              <DateTimePicker
                  onChange={onChange}
                  value={formData.time}
                  name="time"
                  className="form-control" id="time"
              />
            </div>
          </div>
          
          {/* Ugly way to center and give the apropiate size to the submit button using bootstrap */}
          <div className="mb-3 row">
            <div className="col-sm-1"></div>
            <div className="col-sm-10">
              <div className="row">
                <button type="submit" className="btn btn-primary col-sm-12">Calculate delivery price</button>
              </div>
            </div>
            <div className="col-sm-1"></div>
          </div>

          {/* Requst response field */}
          <p>Delivery price: {price}€</p>
        </form>
      </div>
    </div>
  );
}

export default App;
