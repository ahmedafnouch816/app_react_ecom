import React, { useEffect, useState } from "react";

import Header from "../partials/Header";
import Footer from "../partials/Footer";
import { Link } from "react-router-dom";
import useUserData from "../../plugin/useUserData";
import apiInstance from "../../utils/axios";
import moment from "moment";

function Notifications() {

    const [noti , setNoti] = useState([])
    const user_id = useUserData()?.user_id;

    const fetchNoti = async () => {
        try{
            const fetchNoti = await apiInstance.get(`author/dashboard/noti-list/${user_id}/`)
            setNoti(fetchNoti?.data)
            console.log(fetchNoti?.data)
        }catch(err){
            console.log(err)
        }
    }
    useEffect(() => {
        fetchNoti()
    },[]);

    const handleMarkNotiAsSeen = async (noti_id) => {
        try{
            const response = await apiInstance.post(`author/dashboard/noti-mark-seen/${user_id}/`, {noti_id:noti_id})
            console.log(response.data)
            fetchNoti()
            Toast("success", "Notification Seen", "");


        }catch(err){
            console.log(err)
        }
    }

    return (
        <>
            <Header />
            <section className="pt-5 pb-5">
                <div className="container">
                    <div className="row mt-0 mt-md-4">
                        <div className="col-lg-12 col-md-8 col-12">
                            <div className="card mb-4">
                                <div className="card-header d-lg-flex align-items-center justify-content-between">
                                    <div className="mb-3 mb-lg-0">
                                        <h3 className="mb-0">Notifications</h3>
                                        <span>Manage all your notifications from here</span>
                                    </div>
                                </div>
                                <div className="card-body">
                                    <ul className="list-group list-group-flush">
                                    
                                    {noti?.map((c,index) => {
                                        <li className="list-group-item p-4 shadow rounded-3 mt-4">
                                        <div className="d-flex">
                                            <div className="ms-3 mt-2">
                                                <div className="d-flex align-items-center justify-content-between">
                                                    <div>
                                                        <h4 className="mb-0 fw-bold">
                                                            {c.type === "Like" && (
                                                                <>
                                                                <i className="bi bi-chat-left-quote-fill text-success "></i> New Comment 
                                                                </>
                                                            )}
                                                        </h4>

                                                        <h4 className="mb-0 fw-bold">
                                                        {c.type === "Comment" && (
                                                            <>
                                                            <i className="bi bi-chat-left-quote-fill text-success "></i> New Comment 
                                                            </>
                                                        )}
                                                        </h4>


                                                        <h4 className="mb-0 fw-bold">
                                                        {c.type === "Bookmark" && (
                                                            <>
                                                            <i className="bi bi-chat-left-quote-fill text-success "></i> New Bookmark 
                                                            </>
                                                        )}
                                                        </h4>


                                                        <p className="mt-3">
                                                            Monica FineGeh commented on your post <b>How to become a better django and react.js developer</b>
                                                        </p>
                                                    </div>
                                                </div>
                                                <div className="mt-2">
                                                    <p className="mt-1">
                                                        <span className="me-2 fw-bold">
                                                            Date: <span className="fw-light">{moment(n?.date)}</span>
                                                        </span>
                                                    </p>
                                                    <p>
                                                        <button onclick={()=>handleMarkNotiAsSeen(n?.id)} class="btn btn-outline-secondary" type="button">
                                                            Mark as Seen <i className="fas fa-check"></i>
                                                        </button>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                                    })}
                                      {noti?.length === 0 && <p>no notifications yet</p> }    
                                      
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            <Footer />
        </>
    );
}

export default Notifications;
