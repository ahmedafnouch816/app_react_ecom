import { useState, useEffect } from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
import { Link } from "react-router-dom";

import apiInstance from "../../utils/axios";
import useUserData from "../../plugin/useUserData";
import moment from "moment";
import Toast from "../../plugin/Toast";

function Profile() {

    const [profileData, setProfileData] = useState({
        image:null,
        full_name:null,
        about:"",
        bio:"",
        country:""

    });
 


    const user_id = useUserData()?.user_id;

    const [imagePreview, setImagePreview] = useState("");

    const fetchPorilfe = async () => {
        try{
            const response = await apiInstance.get(`user/profile/${user_id}/`)
            setProfileData(response.data);
        }catch(err){
            console.log(err)
        }
 
      
    }

    useEffect(() => {
        fetchPorilfe()
    },[])

    console.log(fetchPorilfe())

    return (
        <>
            <Header />
            <section className="pt-5 pb-5">
                <div className="container">
                    <div className="row mt-0 mt-md-4">
                        <div className="col-lg-12 col-md-8 col-12">
                            <div className="card">
                                <div className="card-header">
                                    <h3 className="mb-0">Profile Details</h3>
                                    <p className="mb-0">You have full control to manage your own account setting.</p>
                                </div>
                                <form className="card-body">
                                    <div className="d-lg-flex align-items-center justify-content-between">
                                        <div className="d-flex align-items-center mb-4 mb-lg-0">
                                            <img src={profileData.image} id="img-uploaded" className="avatar-xl rounded-circle" alt="avatar" style={{ width: "100px", height: "100px", borderRadius: "50%", objectFit: "cover" }} />
                                            <div className="ms-3">
                                                <h4 className="mb-0">Your avatar</h4>
                                                <p className="mb-0">PNG or JPG no bigger than 800px wide and tall.</p>
                                                <input type="file" className="form-control mt-3" name="" id="" />
                                            </div>
                                        </div>
                                    </div>
                                    <hr className="my-5" />
                                    <div>
                                        <h4 className="mb-0 fw-bold">
                                            <i className="fas fa-user-gear me-2"></i>Personal Details
                                        </h4>
                                        <p className="mb-4 mt-2">Edit your personal information and address.</p>
                                        <div className="row gx-3">
                                            <div className="mb-3 col-12 col-md-12">
                                                <label className="form-label" htmlFor="fname">
                                                    Full Name
                                                </label>
                                                <input type="text" id="fname" className="form-control" placeholder="What's your full name?" value={profileData?.full_name || ""} required="" />
                                                <div className="invalid-feedback">Please enter first name.</div>
                                            </div>
                                            <div className="mb-3 col-12 col-md-12">
                                                <label className="form-label" htmlFor="fname">
                                                    Bio
                                                </label>
                                                <input type="text" id="fname" className="form-control" placeholder="Write a catchy bio!" required="" />
                                                <div className="invalid-feedback">Please enter first name.</div>
                                            </div>
                                            <div className="mb-3 col-12 col-md-12">
                                                <label className="form-label" htmlFor="lname">
                                                    About Me
                                                </label>
                                                <textarea placeholder="Tell us about yourself..." name="" id="" cols="30" rows="5" className="form-control"></textarea>
                                                <div className="invalid-feedback">Please enter last name.</div>
                                            </div>

                                            <div className="mb-3 col-12 col-md-12">
                                                <label className="form-label" htmlFor="editCountry">
                                                    Country
                                                </label>
                                                <input type="text" id="country" className="form-control" placeholder="What country are you from?" required="" />
                                                <div className="invalid-feedback">Please choose country.</div>
                                            </div>
                                            <div className="col-12 mt-4">
                                                <button className="btn btn-primary" type="submit">
                                                    Update Profile <i className="fas fa-check-circle"></i>
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <Footer />
        </>
    );
}

export default Profile;
