{/*Component for Wizard form which gathers all necessary user input and sends the user to checkout via Stripe integration. Not Finished, still needs integration into NextJS API's among other logic*/}
import { Radio, 
        FormControlLabel, 
        ToggleButton, 
        Grid, 
        CircularProgress, 
        Step, 
        StepLabel, 
        Stepper, 
        Button, 
       } from '@mui/material';
        
import {Field, Form, Formik, FormikConfig, FormikValues} from 'formik';
import {TextField, RadioGroup, ToggleButtonGroup} from 'formik-mui';
import React, {useState} from 'react';
import CheckoutForm from '../Checkout/OrderSummary';
const sleep = (time) => new Promise((acc) => setTimeout(acc, time));


export default function LensWizard() {

  return(
    <Grid padding={10}>
        <FormikStepper initialValues={{
          //FramType
          frameType: '', //plastic, metal, semi-rimless, rimless --Checkbox
          //FrameDetails
          prescription: false, //Yes or no if their current lenses are presciption --boolean
          satisfied: false, //Are they satisified with their current prescription --boolean
          otherInfo: '', //Additional information that may be helpful --TextBox
          //RxType
          rxType: '', //Single Vision(far sighted or near sighted OR reading glasses),  Progressive, Bifocal --Checkbox
          //Prescription Information
          prescriptionInfo: '', //Upload their Rx, enter manually or let the lab figure out current Rx --Checkbox
          //Lens Options
          lensOptions: '', //CR39 Plastic, Polycarbonate, Trivex, 1.67HighIndex, 1.74HighIndex, 1.7HighIndex. --Checkbox
          //LensUpgrades
          antiReflective: '',  //Standard, Premium -- Checkbox
          lensType: '', //Clear, Blu-light Blocking, Sunglass, Transitions --Checkbox
          edgeOptions: '', //none, Polish Edges --Checkbox
          specialUpgradeRequests: '', //If they have any other upgrade requests not listed. --Textbox
          country: '',
          name: '',
          address: '',
          city: '',
          zipCode: '',
          emailAddress: '',
          phoneNumber: '',
          orderNotes: '',

        }} onSubmit={async (values) => {
          await sleep(3000);
          console.log('values', values);
        }}>
        <Grid item align="center" padding={5} className="col-lg-12 col-md-12">

          <FormikStep label="Frame Type">


          <a>Frame Type</a>
            <Field 
              id="frameType"
              name="frameType" 
              type="checkbox" 
              component={ToggleButtonGroup} 
              exclusive
              Label={{label: 'frameType'}} 
              labelId="frameType">
                
              <ToggleButton value="plastic" >Plastic</ToggleButton>
              <ToggleButton value="metal">Metal</ToggleButton>
              <ToggleButton value="semiRimless">Semi Rimless</ToggleButton>
              <ToggleButton value="rimless">Rimless</ToggleButton>
           
            </Field>

            </FormikStep>
            </Grid>

            <FormikStep label="Lens Information">
            <Grid item display="flex" justifyContent="center" padding={5}>

            <a>Are the lens prescription?</a>
            <Field 
              id="prescription"
              name="prescription" 
              type="checkbox" 
              component={RadioGroup}
              alignItems="center"
              display="flex"
              justifyContent="space-between"
              Label={{label: 'prescription'}} 
              labelId="prescription">
              <FormControlLabel value="prescriptionYes"  control={<Radio align="center" />} label="Yes" />
              <FormControlLabel value="prescriptionNo" control={<Radio />} label="No" />
            
            </Field>
            
            <a>Are you satisified with your current prescription?</a>
            <Field 
              id="satisified"
              name="satisified" 
              type="checkbox" 
              component={RadioGroup} 
              Label={{label: 'Satisified with Current Prescription?'}} 
              labelId="satisfied">
 
              <FormControlLabel value="satisfiedYes" control={<Radio />} label="Yes" />
              <FormControlLabel value="satisifiedNo" control={<Radio />} label="No" />
 
            </Field>
            <Field name="otherInfo" component={TextField} label="otherInfo"/>
            </Grid>

            </FormikStep>

            <FormikStep label='Rx Type'>

            <Grid item align="center" padding={5}>
            <a>Please select Your Rx Type</a>  

            <Field //Single Vision(far sighted or near sighted OR reading glasses),  Progressive, Bifocal --Checkbox
              id="rxType"
              name="rxType" 
              type="checkbox" 
              component={ToggleButtonGroup} 
              exclusive
              Label={{label: 'rxType'}} 
              labelId="rxType">
             
              <ToggleButton value="singleVision" >Single Vision</ToggleButton>
              <ToggleButton value="progressive" >Progressive</ToggleButton>
              <ToggleButton value="bifocal" >Bifocal</ToggleButton>
           
            </Field>
            </Grid>
            </FormikStep>
            <FormikStep label='Rx Information'>
            <Grid item display="flex" justifyContent="center" padding={5} >
            <a>Please Enter your Prescription or upload a PDF or image of it</a>

            <Field //Upload their Rx, enter manually or let the lab figure out current Rx --Checkbox
              id="prescriptionInfo"
              name="prescriptionInfo" 
              type="checkbox" 
              component={RadioGroup} 
              Label={{label: 'prescriptionInfo'}} 
              labelId="prescriptionInfo">
              <FormControlLabel value="uploadRx" control={<Radio />} label="Upload RX (RECOMMENDED)" /> 
              <FormControlLabel value="manualRx" control={<Radio />} label="Manually Enter RX" />
              <FormControlLabel value="labRx" control={<Radio />} label="Let us Determine RX" />

            </Field>
            </Grid>
            </FormikStep>
            <FormikStep label="Lens Options">
            <Grid item display="flex" justifyContent="center" padding={5}> 
            <a>Select your lens options</a>

             {/* //CR39 Plastic, Polycarbonate, Trivex, 1.67HighIndex, 1.74HighIndex, 1.7HighIndex. --Checkbox */}
              <Field
              id="lensOptions"
              name="lensOptions" 
              type="checkbox" 
              component={RadioGroup} 
              Label={{label: 'lensOptions'}} 
              labelId="lensOptions">
              <FormControlLabel value="cr39Plastic" control={<Radio />} label="CR39 Plastic" /> 
              <FormControlLabel value="polycarbonate" control={<Radio />} label="Polycarbonate" />
              <FormControlLabel value="trivex" control={<Radio />} label="Trivex" />
              <FormControlLabel value="167highIndex" control={<Radio />} label="1.67 High Index" />
              <FormControlLabel value="174highIndex" control={<Radio />} label="1.74 High Index" />
              <FormControlLabel value="17highIndex" control={<Radio />} label="1.7 High Index" />

            </Field>
            </Grid>
            </FormikStep>
            <FormikStep label='Lens Upgrades'>
            <Grid item display="flex" justifyContent="center" padding={5} className="col-lg-12">
            <a>Select the upgrades you want</a>

                <Field
                  id="antiReflective"
                  name="antiReflective" 
                  type="checkbox" 
                  component={RadioGroup} 
                  Label={{label: 'antiReflective'}} 
                  labelId="antiReflective">
                  <FormControlLabel value="standard" control={<Radio />} label="Standard" /> 
                  <FormControlLabel value="premium" control={<Radio />} label="Premium" />

                </Field>
                <Field
                  id="lensType"
                  name="lensType" 
                  type="checkbox" 
                  component={RadioGroup} 
                  Label={{label: 'lensType'}} 
                  labelId="lensType">
                  <FormControlLabel value="clear" control={<Radio />} label="Clear" /> 
                  <FormControlLabel value="blueLight" control={<Radio />} label="Blue Light" />
                  <FormControlLabel value="blocking" control={<Radio />} label="Blocking" />
                  <FormControlLabel value="sunglass" control={<Radio />} label="Sunglass" />
                  <FormControlLabel value="transitions" control={<Radio />} label="Transitions" />

                </Field>            
                <Field
                  id="edgeOptions"
                  name="edgeOptions" 
                  type="checkbox" 
                  component={RadioGroup} 
                  Label={{label: 'edgeOptions'}} 
                  labelId="edgeOptions">
                  <FormControlLabel value="noPolish" control={<Radio />} label="Don't Polish Edges" /> 
                  <FormControlLabel value="polishEdges" control={<Radio />} label="Polish Edges" />

                </Field>
                <Field name="specialUpgradeRequests" component={TextField} label="specialUpgradeRequests"/>
                
          </Grid>
          </FormikStep>
          {/* country: '',
          name: '',
          address: '',
          city: '',
          zipCode: '',
          emailAddress: '',
          phoneNumber: '',
          orderNotes: '', */}
          <FormikStep label="Billing and Shipping">
            <Grid item display="flex" justifyContent="space-between" flexDirection="column" padding={5}>
              <Field name="country" component={TextField} label="country"/>
              <Field name="name" component={TextField} label="name"/>
              <Field name="address" component={TextField} label="address"/>
              <Field name="city" component={TextField} label="city"/>
              <Field name="zipCode" component={TextField} label="zipCode"/>
              <Field name="emailAddress" component={TextField} label="emailAddress"/>
              <Field name="phoneNumber" component={TextField} label="phoneNumber"/>
              <Field name="orderNotes" component={TextField} label="orderNotes"/>
            </Grid>
          <CheckoutForm></CheckoutForm>
          </FormikStep>

        </FormikStepper>
    </Grid>
    
  );
}

export interface FormikStepProps
  extends Pick<FormikConfig<FormikValues>, 'children' | 'validationSchema'> {
  label: string;
}

export function FormikStep({ children }: FormikStepProps) {
  return <>{children}</>;
}

export function FormikStepper({ children, ...props }: FormikConfig<FormikValues>) {
  const childrenArray = React.Children.toArray(children) as React.ReactElement<FormikStepProps>[];
  const [step, setStep] = useState(0);
  const currentChild = childrenArray[step];
  const [completed, setCompleted] = useState(false);

  function isLastStep() {
    return step === childrenArray.length - 1;
  }
  return (
    <Formik
      {...props}
      validationSchema={currentChild.props.validationSchema}
      onSubmit={async (values, helpers) => {
        if (isLastStep()) {
          await props.onSubmit(values, helpers);
          setCompleted(true);
        } else {
          setStep((s) => s + 1);
          helpers.setTouched({});
        }
      }}
    >
      {({ isSubmitting }) => (
        <Form autoComplete="off">
          <Stepper alternativeLabel activeStep={step}>
            {childrenArray.map((child, index) => (
              <Step key={child.props.label} completed={step > index || completed}>
                <StepLabel>{child.props.label}</StepLabel>
              </Step>
            ))}
          </Stepper>

          {currentChild}

          <Grid container spacing={2} alignItems="center" justifyContent="center">
            {step > 0 ? (
              <Grid item >
                <Button
                  disabled={isSubmitting}
                  variant="contained"
                  color="primary"
                  onClick={() => setStep((s) => s - 1)}
                >
                  Back
                </Button>
              </Grid>
            ) : null}
            <Grid item >
              <Button
                startIcon={isSubmitting ? <CircularProgress size="1rem" /> : null}
                disabled={isSubmitting}
                variant="contained"
                color="primary"
                type="submit"
              >
                {isSubmitting ? 'Submitting' : isLastStep() ? 'Submit' : 'Next'}
              </Button>
            </Grid>
          </Grid>
        </Form>
      )}
    </Formik>
  );
}



