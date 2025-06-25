import kfp
from kfp import dsl
from kubernetes.client.models import V1EnvVar, V1EnvVarSource, V1SecretKeySelector


# Function to inject DagsHub secrets
def add_dagshub_env(op: dsl.ContainerOp):
    return op.add_env_variable(V1EnvVar(
                name='DAGSHUB_USERNAME',
                value_from=V1EnvVarSource(
                    secret_key_ref=V1SecretKeySelector(
                        name='dagshub-secret',  # Name of your Kubernetes Secret
                        key='DAGSHUB_USERNAME'  # Key inside that secret
                    )
                )
            )).add_env_variable(V1EnvVar(
                name='DAGSHUB_TOKEN',
                value_from=V1EnvVarSource(
                    secret_key_ref=V1SecretKeySelector(
                        name='dagshub-secret',
                        key='DAGSHUB_TOKEN'
                    )
                )
            ))


def data_processing_op():
    op = dsl.ContainerOp(
        name="Data Processing",
        image="avnishsingh17/cancer_survival2:latest",
        command=["python", "src/data_preprocessing.py"]
    )
    return add_dagshub_env(op)


def model_training_op():
    op = dsl.ContainerOp(
        name="Model Training",
        image="avnishsingh17/cancer_survival:latest",
        command=["python", "src/model_training.py"]
    )
    return add_dagshub_env(op)


### pipeline start here

@dsl.pipeline(
    name="MLOps pipeline",
    description="This is a Kubeflow pipeline"
)
def mlops_pipeline():
    data_processing = data_processing_op()
    model_training = model_training_op().after(data_processing)


### RUN the pipeline

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        mlops_pipeline, "mlops_pipeline.yaml"
    )
