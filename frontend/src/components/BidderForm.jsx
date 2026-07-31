import { useState } from "react";

function BidderForm({

    onSubmit,

    buttonText

}) {

    const [bidderName, setBidderName] = useState("");

    const [contactPerson, setContactPerson] = useState("");

    const [email, setEmail] = useState("");

    const [phone, setPhone] = useState("");

    async function submitForm(e) {

        e.preventDefault();

        if (!bidderName.trim()) {

            alert(
                "Bidder Name is required."
            );

            return;

        }

        await onSubmit({

            bidder_name: bidderName,

            contact_person: contactPerson,

            email: email,

            phone: phone

        });

    }

    return (

        <form onSubmit={submitForm}>

            <div className="mb-3">

                <label className="form-label">

                    Bidder Name

                </label>

                <input
                    className="form-control"
                    value={bidderName}
                    onChange={(e) =>
                        setBidderName(
                            e.target.value
                        )
                    }
                    required
                />

            </div>

            <div className="mb-3">

                <label className="form-label">

                    Contact Person

                </label>

                <input
                    className="form-control"
                    value={contactPerson}
                    onChange={(e) =>
                        setContactPerson(
                            e.target.value
                        )
                    }
                />

            </div>

            <div className="mb-3">

                <label className="form-label">

                    Email

                </label>

                <input
                    type="email"
                    className="form-control"
                    value={email}
                    onChange={(e) =>
                        setEmail(
                            e.target.value
                        )
                    }
                />

            </div>

            <div className="mb-3">

                <label className="form-label">

                    Phone

                </label>

                <input
                    className="form-control"
                    value={phone}
                    onChange={(e) =>
                        setPhone(
                            e.target.value
                        )
                    }
                />

            </div>

            <button
                className="btn btn-primary"
                type="submit"
            >

                {buttonText}

            </button>

        </form>

    );

}

export default BidderForm;